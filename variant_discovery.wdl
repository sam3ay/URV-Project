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
  String google_apiKey
  String dataproc_cluster

  String? runner
  String? mem
  String? cores
  
  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        input_bam=inputbamarray[i][0]
        ref_fasta=ref_fasta
        known_variants=known_variants
        output_name=inputbamarray[i][1]
        google_apiKey=google_apiKey
        dataproc_cluster=dataproc_cluster
        runner=runner
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
  String Output
  
  String? google_apiKey
  String? runner
  String? dataproc_cluster
  String? mem
  String? cores
  String java_opt

  
  command {
    set -e
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk4_jar_override}
      gatk \
      ReadsPipelineSpark \
      --input ${input_bam} \
      --knownSites ${known_variants} \
      --output "${output}.vcf" \
      --reference ${ref_fasta} \
      --apiKey ${google_apiKey} \
      -align \
      -- \
      --sparkRunner ${runner} \
      --cluster ${dataproc_cluster}
  }
  runtime {
    appMainClass: "org.broadinstitute.hellbender.Main"
    executorMemory: select_first([mem, "4G"])
    executorCores: select_first([cores, "2"])
  }
  output {
    File rawVCF = "${output}.vcf"
  }
}
