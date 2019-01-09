## Based on Broad Institutes GATK4 best preactices
## Requirements/expectations:
## - Pair-end sequencing data in unmapped bam
## - Input bam Requirements
## - - filenames all have the same suffix (use ".unmapped.bam")
## - - files must pass validation by ValidateSamFile
## - - reads are provided in query-sorted order
## - - all reads must have an RG tag
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

  Boolean? create_dataproc
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
  String? initaction
  String? metadata
  String? image_ver
  String? conf
  String? service_account
  String? fair_location
  String? scheduler
  String? json_location

  # gcs copy Variables
  String gcs_dir
  String hdfs_out="hdfs://${cluster_name}-m:8020/${project}"
  # ReadsPipelineSpark inputs
  # If gs:// links keep as strings, if local change to files
  File bamtsv
  Array[Array[String]] inputbamarray = read_tsv(bamtsv)
  String ref_fasta
  String known_variants
  String dbsnp
  Boolean? shard_output
  String outputpath
  String vcf_list_name

  # local gatk
  File? gatk_jar
  File? gatk_path

  # spark properties
  String? execmem           # memory per executor (~90% of worker mem/3)
  Int? numexec              # total number of executors (3 per node generally)
  Int? execores             # cores per executor (5 per executor)
  String? drivermem         # used to bolster yarn node manager
  Int? drivercores

  if (select_first([create_dataproc, true])) {
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
        scheduler=scheduler,
        fair_location=fair_location,
        json_location=json_location,
        max_age=max_age
    }
  }
  
  call CopyGCSDirIntoHDFSSpark {
    input:
      gatk_path=gatk_path,
      gatk_jar=gatk_jar,
      gcs_dir=gcs_dir,
      outputpath=outputpath,
      project=project,
      hdfs_out=hdfs_out,
      cluster_name=CreateCluster.cluster_name
  }

  scatter (i in range(length(inputbamarray))) {
    call ReadsPipelineSpark {
      input:
        gatk_jar=gatk_jar,
        gatk_path=gatk_path,
        hdfs_path=CopyGCSDirIntoHDFSSpark.hdfs_path,
        input_bam=inputbamarray[i][0],
        sample=inputbamarray[i][1],
        ref_fasta=ref_fasta,
        known_variants=known_variants,
        dbsnpvcf=dbsnp,
        shard_output=shard_output,
        drivercores=drivercores,
        outputpath=outputpath,
        cluster_name=cluster_name,
        project=project,
        execmem=execmem,
        numexec=numexec,
        execores=execores,
        drivermem=drivermem,
        fair_location=fair_location,
        conf=conf
    }
  }
  call CopyHDFSIntoGCS {
    input:
      vcf=ReadsPipelineSpark.VCF,
      vcf_list=vcf_list_name,
      outputpath=outputpath,
      hdfs_path=CopyGCSDirIntoHDFSSpark.hdfs_path
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
  String? initaction
  String? metadata
  String? json_location
  String? fair_location
  String? scheduler
  String? service_account
  String? image_ver

  command <<<
  set -eu
  gcloud beta dataproc clusters create ${cluster} \
    --bucket ${bucket} \
    --region ${default="global" region} \
    --zone ${default="us-west1-b" zone} \
    --master-machine-type ${default="n1-highmem-8" mastermachinetype} \
    --master-boot-disk-size ${default=800 masterbootdisk} \
    --num-workers ${default=6 numworker} \
    --worker-machine-type ${default="n1-highmem-8" workermachinetype} \
    --worker-boot-disk-size ${default=800 workerbootdisk} \
    --project ${project} \
    --async \
    --scopes ${default="default,cloud-platform,storage-full" scopes} \
    --max-idle ${default="600s" max_idle} \
    --max-age ${default="24h" max_age} \
    --initialization-actions ${initaction} \
    --image-version ${default="1.3-deb9" image_ver} \
    --metadata service_account="${service_account},json_location=${json_location},scheduler=${scheduler},schedule_location=${fair_location},${metadata}" \
    --properties "dataproc:dataproc.logging.stackdriver.enable=true,dataproc:dataproc.monitoring.stackdriver.enable=true,yarn:yarn.resourcemanager.scheduler.class=org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler,yarn:yarn.scheduler.fair.user-as-default-queue=false"
  >>>
  output {
    String cluster_name = "${cluster}"
  }
}
task CopyGCSDirIntoHDFSSpark {

  String gcs_dir
  String cluster_name
  String project
  String hdfs_out
  
  File? gatk_jar
  File? gatk_path
  String? outputpath

  command <<<
    set -eu
    export GATK_GCS_STAGING="${outputpath}/"
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk_jar}
    ${default="gatk" gatk_path} \
      ParallelCopyGCSDirectoryIntoHDFSSpark \
        --input-gcs-path "${gcs_dir}" \
        --output-hdfs-directory "${hdfs_out}" \
        -- \
        --spark-runner GCS \
        --cluster "${cluster_name}"
  >>>
  output {
      String hdfs_path = "${hdfs_out}"
  }
}
# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  String input_bam
  String ref_fasta
  String hdfs_path
  String known_variants
  String dbsnpvcf
  String sample
  String cluster_name
  String project
  String? conf
  String? fair_location
  Boolean? shard_output
  String? execmem           # memory per executor (~90% of worker mem/3)
  Int? numexec              # total number of executors (3 per node generally)
  Int? execores             # cores per executor (5 per executor)
  String? drivermem         # used to bolster yarn node manager
  Int? drivercores


  File? gatk_jar
  File? gatk_path
  String outputpath

  # spark calcs assuming 52 gbs per worker total worker 6
  # want no more than 5 executors per node 2 by default
  #--verbosity=debug \

  command <<<
    set -eu
    export GATK_GCS_STAGING="${outputpath}/"
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk_jar}
    ${default="gatk" gatk_path} \
      ReadsPipelineSpark \
        --input "${hdfs_path}/${sample}.unmapped.bam" \
        --known-sites "${hdfs_path}/${known_variants}" \
        --output "${hdfs_path}/vcf/${sample}.vcf" \
        --reference "${hdfs_path}/${ref_fasta}" \
        --dbsnp "${hdfs_path}/${dbsnpvcf}" \
        --sharded-output ${default='true' shard_output} \
        --align \
        -- \
        --spark-runner GCS \
        --cluster ${cluster_name} \
        --num-executors ${default=12 numexec} \
        --executor-cores ${default=2 execores} \
        --executor-memory ${default="10G" execmem} \
        --driver-memory ${default="10G" drivermem} \
        --driver-cores ${default=4 drivercores} \
        --conf "spark.dynamicAllocation.enabled=false,spark.yarn.executor.memoryOverhead=10240"
  >>>
  output {
    String VCF = "${hdfs_path}/vcf/${sample}.vcf"
  }
}

task CopyHDFSIntoGCS {
  Array[String] vcf
  String vcf_list
  String hdfs_path
  String outputpath

  command {
    mv ${write_lines(vcf)} ${vcf_list}.list && \
    gcloud dataproc jobs submit pig --execute "sh hadoop distcp ${hdfs_path}/vcf/ ${outputpath}/"
  }
  output {
    File vcf_out_list = "${vcf_list}.list"
  }
}
