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
## - Successfully tested on v36
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
  # If gs:// links keep as strings, if local change to files
  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  String ref_fasta
  String known_variants
  String outputpath

  # local gatk
  File? gatk_jar

  # runtime
  String? gatk_docker
  String? gcloud_docker
  Int? mem
  Int? cpu
  Int? disk

  call CreateCluster {
    input:
      cluster=cluster_name,
      bucket=bucket_name,
      region=region,
      zone=zone,
      mastermachinetype=mastermachinetype,
      workermachinetype=workermachinetype,
      masterbootdisk=masterbootdisk,
      workerbootdisk=workerbootdisk,
      numworker=numworker,
      project=project,
      scopes=scopes,
      max_idle=max_idle,
      max_age=max_age,
      gcloud_docker=gcloud_docker,
      mem=mem,
      cpu=cpu,
      disk=disk
  }
  
  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        input_bam=inputbamarray[i][0],
        ref_fasta=ref_fasta,
        known_variants=known_variants,
        sample=inputbamarray[i][1],
        gatk_jar=gatk_jar,
        outputpath=outputpath,
        cluster_name=cluster_name,
        gatk_docker=gatk_docker,
        mem=mem,
        cpu=cpu,
        disk=disk
    }
  }
}

# TASK DEFITIONS

# Create Dataproc cluster
task CreateCluster {
  
  # Inputs for this task
  String cluster
  String bucket
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

  # runtime 
  String? gcloud_docker
  Int? mem
  Int? cpu
  Int? disk

  command <<<
  set -eu
  gcloud --project ${project} beta dataproc clusters create ${cluster} \
    --bucket ${bucket} \
    --region ${default="us-west1" region} \
    --zone ${default="us-west1-b" zone} \
    --master-machine-type ${default="n1-standard-8" mastermachinetype} \
    --master-boot-disk-size ${default=100 masterbootdisk} \
    --num-workers ${default=5 numworker} \
    --worker-machine-type ${default="n1-standard-8" workermachinetype} \
    --worker-boot-disk-size ${default=50 workerbootdisk} \
    --async \
    --scopes ${default="default,cloud-platform,storage-full" scopes} \
    --max-idle ${default="t10m" max_idle} \
    --max-age ${default="4h" max_age}
  >>>
  runtime {
    docker: select_first([gcloud_docker, "google/cloud-sdk:latest"])
    memory: select_first([mem, 2]) + " GB"
    cpu: select_first([cpu, 1])
    disks: "local-disk " + select_first([disk, 10]) + " HDD"
  }
  output {
    String Dataproc_Name = "${cluster}"
  }
}
# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  String input_bam
  String ref_fasta
  String known_variants
  String sample
  String cluster_name

  File? gatk_jar
  String outputpath

  # runtime
  String? gatk_docker
  Int? mem
  Int? cpu
  Int? disk

  command <<<
    set -eu
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk_jar}
    gatk \
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
    docker: select_first([gatk_docker, "broadinstitute/gatk:latest"])
    memory: select_first([mem, 2]) + " GB"
    cpu: select_first([cpu, 1])
    disks: "local-disk " + select_first([disk, 10]) + " HDD"
  }
  output {
    String VCF = "${outputpath}${sample}.vcf" 
  }
}
