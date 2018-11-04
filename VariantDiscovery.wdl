## Based on Broad Institutes GATK4 best preactices
## Requirements/expectations:
## - Pair-end sequencing data in unmapped bam
## - Input bam Requirements
## - - filenames all have the same suffix (use ".unmapped.bam")
## - - files must pass validation by ValidateSamFile
## - - reads are provided in query-sorted order
## - - all reads must have an RG tag
## - Local environment must contain
## Output :
## - Filtered VCF file and its index, filtered using variant quality score recalibration
##   (VQSR). All sites that are present in the input VCF are retained.
##   Filtered sites are annotated as such in the FILTER field.
##
## Software version requirements
## - GATK4.beta.3 or later
## - Samtools (see gotc docker)
## - Python 2.7 & Python 3.6
##
## Cromwell version support 
## - Successfully tested on v29 
## - Does not work on versions < v23 due to output syntax

# Workflow Definition
workflow ReadsPipelineSparkWorkflow {

  # ReadsPipelineSpark inputs
  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  File ref_fasta
  File known_variants
  String outputpath
  String runner
  String cluster_name

  String gatk_path

  # runtime params
  String? mem
  Int? cores

  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        input_bam=inputbamarray[i][0],
        ref_fasta=ref_fasta,
        known_variants=known_variants,
        sample=inputbamarray[i][1],
        gatk_path=gatk_path,
        outputpath=outputpath,
        cluster_name=cluster_name,
        runner=runner,
        mem=mem,
        cores=cores
    }
  }
}

# TASK DEFITIONS

# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  File input_bam
  File ref_fasta
  File known_variants
  String sample
  String cluster_name
  String runner

  String gatk_path
  String outputpath

  # runtime params
  # expecting 5 workers n8-standard
  String? mem
  Int? cores
  
  command <<<
    set -eu
    ${gatk_path} \
      ReadsPipelineSpark \
        --input ${input_bam} \
        --knownSites ${known_variants} \
        --output "${outputpath}${sample}.vcf" \
        --reference ${ref_fasta} \
        --align \
        -- \
        --spark-runner runner \
        --cluster ${cluster_name}
  >>>
  runtime {
    appMainClass: "org.broadinstitute.hellbender.Main"
    executorMemory: select_first([mem, "7GB"])
    executorCores: select_first([cores, "20"])
  }
  output {
    File VCF = "${outputpath}${sample}.vcf" 
  }
}
