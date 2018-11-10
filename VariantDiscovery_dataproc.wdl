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
## --gcs-project-for-requester-pays ${project} \

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
  String initaction
  String? metadata
  String? image_ver
  String? conf

  # ReadsPipelineSpark inputs
  # If gs:// links keep as strings, if local change to files
  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  String ref_fasta
  String known_variants
  String outputpath
  String service_account
  String json_location

  # local gatk
  File? gatk_jar
  File? gatk_path

  # spark properties
  String? execmem           # memory per executor (~90% of worker mem/3)
  Int? numexec              # total number of executors (3 per node generally)
  Int? execores             # cores per executor (5 per executor)
  String? drivermem         # used to bolster yarn node manager

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
      service_account=service_account,
      scopes=scopes,
      max_idle=max_idle,
      initaction=initaction,
      image_ver=image_ver,
      metadata=metadata,
      json_location=json_location,
      max_age=max_age
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
        project=project,
        execmem=execmem,
        numexec=numexec,
        execores=execores,
        drivermem=drivermem,
        conf=conf,
        gatk_path=gatk_path
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
  String initaction
  String? metadata
  String json_location
  String service_account
  String? image_ver

  command <<<
  set -eu
  gcloud beta dataproc clusters create ${cluster} \
    --bucket ${bucket} \
    --region ${default="global" region} \
    --zone ${default="us-west1-b" zone} \
    --master-machine-type ${default="n1-standard-4" mastermachinetype} \
    --master-boot-disk-size ${default=100 masterbootdisk} \
    --num-workers ${default=5 numworker} \
    --worker-machine-type ${default="n1-highmem-8" workermachinetype} \
    --worker-boot-disk-size ${default=500 workerbootdisk} \
    --project ${project} \
    --async \
    --scopes ${default="default,cloud-platform,storage-full" scopes} \
    --max-idle ${default="600s" max_idle} \
    --max-age ${default="12h" max_age} \
    --initialization-actions ${initaction} \
    --image-version ${default="1.3-deb9" image_ver} \
    --metadata service_account="${service_account},json_location=${json_location},${metadata}"
  >>>
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
  String project
  String? conf
  String? execmem           # memory per executor (~90% of worker mem/3)
  Int? numexec              # total number of executors (3 per node generally)
  Int? execores             # cores per executor (5 per executor)
  String? drivermem         # used to bolster yarn node manager


  File? gatk_jar
  File? gatk_path
  String outputpath

  # spark calcs assuming 52 gbs per worker
  # want no more than 5 executors per node


  command <<<
    set -eu
    export GATK_GCS_STAGING="${outputpath}"
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk_jar}
    ${default="gatk" gatk_path} \
      ReadsPipelineSpark \
        --input ${input_bam} \
        --known-sites ${known_variants} \
        --output "${outputpath}/vcf/${sample}.vcf" \
        --reference ${ref_fasta} \
        --align \
        -- \
        --spark-runner GCS \
        --cluster ${cluster_name} \
        --num-executors ${default=15 numexec} \
        --executor-cores ${default=5 execores} \
        --executor-memory ${default="16G" execmem} \
        --driver-memory ${default="4G" drivermem} \
        --conf ${default="spark.dynamicAllocation.enabled=false" conf}
  >>>
  output {
    String VCF = "${outputpath}${sample}.vcf" 
  }
}
