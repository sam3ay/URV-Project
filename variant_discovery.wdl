## Based on Broad Institutes GATK4 best preactices
## Requirements/expectations:
## - Pair-end sequencing data in unmapped bam
## - Input bam Requirements
## -- filenames all have the same suffix (use ".unmapped.bam")
## -- files must pass validation by ValidateSamFile
## -- reads are provided in query-sorted order
## -- all reads must have an RG tag
## Output :
## - Clean BAM file and its index, suitable for variant discovery analyses.
## - VCF file and its index
## - Filtered VCF file and its index, filtered using variant quality score recalibration
##   (VQSR) with genotypes for all samples present in the input VCF. All sites that 
##   are present in the input VCF are retained; filtered sites are annotated as such 
##   in the FILTER field.
##
## Software version requirements (see recommended dockers in inuts JSON)
## - GATK4.beta.3 or later
## - Samtools (see gotc docker)
## - Python 2.7 & Python 3.6
##
## Cromwell version support 
## - Successfully tested on v29 
## - Does not work on versions < v23 due to output syntax

# Workflow Definition
workflow ReadsPipelineSparkWorkflow {

  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  File ref_fasta
  File known_variants

  String gatk_path
  bucketpath

  # spark params
  String runner

  # runtime params
  String? execnum
  String? mem
  String? cores
  
  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        input_bam=inputbamarray[i][0]
        ref_fasta=ref_fasta
        known_variants=known_variants
        sample=inputbamarray[i][1]
        gatk_path=gatk_path
        bucketpath=bucketpath
        runner=runner
        execnum=execnum
        mem=mem
        cores=cores
    }
  }
}
# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  File input_bam
  File ref_fasta
  File known_variants
  String sample

  String gatk_path
  bucketpath

  # spark params
  String runner
  String? execnum
  String? mem
  String? cores
  
  command <<<
    set -e
    ${gatk_path} \
      ReadsPipelineSpark \
        --input ${input_bam} \
        --knownSites ${known_variants} \
        --output "${bucketpath}${sample}.vcf" \
        --reference ${ref_fasta} \
        --align \
        -- \
        --spark-runner ${runner} \
  >>>
  runtime {
    appMainClass: "org.broadinstitute.hellbender.Main"
    numberOfExecutors: select_first([execnum, "7"])
    executorMemory: select_first([mem, "4G"])
    executorCores: select_first([cores, "3"])
  }
  output {
    File VCF = "${bucketpath}${sample}.vcf" \

  }
}
