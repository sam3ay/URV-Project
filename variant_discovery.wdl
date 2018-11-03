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
## - Google Cloud SDK (ver 223.0.0 or later)
##
## Cromwell version support 
## - Successfully tested on v29 
## - Does not work on versions < v23 due to output syntax

# Workflow Definition
workflow ReadsPipelineSparkWorkflow {

  # Dataproc settings
  String cluster_name
  String bucket_name
  String project
  String? region
  String? zone
  String? mastermachinetype
  Int? masterbootdisk
  String? workermachinetype
  Int? workerbootdisk
  Int? numworker
  String? max_idle
  String? max_age
  String? scopes

  # ReadsPipelineSpark inputs
  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  File ref_fasta
  File known_variants
  String outputpath

  String gatk_path

  # runtime params
  String mem
  Int cores

  call CreateCluster {
    input:
      cluster=cluster_name
      bucket=bucket_name
      region=region
      zone=zone
      mastermachinetype=mastermachinetype
      workermachinetype=workermachinetype
      masterbootdisk=masterbootdisk
      workerbootdisk=workerbootdisk
      numworker=numworker
      project=project
      scopes=scopes
      max_idle=max_idle
      max_age=max_age
  }
  
  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        input_bam=inputbamarray[i][0]
        ref_fasta=ref_fasta
        known_variants=known_variants
        sample=inputbamarray[i][1]
        gatk_path=gatk_path
        outputpath=outputpath
        cluster_name=cluster_name
        mem=mem
        cores=cores
    }
  }
}

# TASK DEFITIONS

# Create Dataproc cluster
task CreateCluster {
  
  # Inputs for this task
  String cluster_name
  String bucket_name
  String project
  String? region
  String? zone
  String? mastermachinetype
  Int? masterbootdisk
  Int? numworker
  String? workermachinetype
  Int? workerbootdisk
  String? max_idle
  String? max_age
  String? scopes

  # runtime params
  String mem
  Int cores

  command <<<
  set -e
  gcloud beta dataproc clusters create ${cluster_name}\
    --bucket ${bucket_name}\
    --region ${default="us-west" region} \
    --zone ${default="us-west1-b" zone} \
    --master-machine-type ${default="n1-highmem-8" mastermachinetype} \
    --master-boot-disk-size ${default=500 masterbootdisk} \
    --num-workers ${default=10 numworker} \
    --worker-machine-type ${default="n1-highmem-8" workermachinetype} \
    --worker-boot-disk-size ${default=50 workerbootdisk} \
    --project ${project} \
    --async \
    --scopes ${default="default,cloud-platform,storage-full" scopes}\
    --max-idle ${default="t10m" max_idle} \
    --max-age ${default="4h" max_age}
  >>>

  runtime {
    memory: mem
    cpu: cores
  }
}
# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  File input_bam
  File ref_fasta
  File known_variants
  String sample
  String cluster_name

  String gatk_path
  outputpath

  # runtime params
  String mem
  Int cores
  
  command <<<
    set -e
    ${gatk_path} \
      ReadsPipelineSpark \
        --input ${input_bam} \
        --knownSites ${known_variants} \
        --output "${outputpath}${sample}.vcf" \
        --reference ${ref_fasta} \
        --align 
        -- \
        --spark-runner GCS \
        --cluster ${cluster_name}
  >>>
  runtime {
    memory: mem
    cpu: cores
  }
  output {
    File VCF = "${outputpath}${sample}.vcf" 
  }
}
