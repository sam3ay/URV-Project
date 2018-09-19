## This WDL converts a fastq file to uBAMs, one per readgroup 
## 
## Requirements/expectations : 
## - Pair-end sequencing data in fq.gz format 
## - One or more read groups 
##
## Outputs : 
## - Set of unmapped BAMs, one per read group
##
## Cromwell version support 
## - Successfully tested on v27
## - Does not work on versions < v23 due to output syntax

# Workflow Definition
workflow fastqconversion {
  # TSV File contains inputFastqarray name; fastq1; fastq2; read_group;unmapped_bam output
  File fastqTsv
  Array[Array[String]] inputFastqarray = read_tsv(fastqTsv)
  String ubam_list_name = basename(readgroup_list,".list")


  String docker
  Int? preemptible_attempts


  # run multiple fastq pair conversions in parallel
  scatter (i in range(length(inputFastqarray))) {


    # Convert pair of FASTQs to uBAM
    call FastqToSam {
      sample_name=inputFastqarray[i][0],
      fastq1=inputFastqarray[i][0],
      fastq2=inputFastqarray[i][1],
      output=inputFastqarray[i][2]
      platform= "illumina",
      platform_model=inputFastqarray[i][24],
      library_name=inputFastqarray[i][13],
      sequencing_center=inputFastqarray[i][4],
      readgroup=inputFastqarray[i][3],
      predictedinsertsize = inputFastqarray[2],
      comment=inputFastqarray[i][8]
      docker = docker,
      preemptible_attempts = preemptible_attempts
    }
  }

# Create a list with the generated ubams
    call CreateUbamList {
      input:
        unmapped_bams = FastqToSam.output_bam,
        ubam_list_name = ubam_list_name,
        docker = docker,
        preemptible_attempts = preemptible_attempts
    }
# Outputs that will be retained when execution is complete
    output {
      Array[File] output_bams = FastQsToUnmappedBAM.output_bam
      File unmapped_bam_list = CreateUbamList.unmapped_bam_list
    }
}


# TASK DEFINITION


# Convert Fastq files to uBAMs 
task FastToSam {
  File fastq1
  File fastq2
  String platform
  String platform_model
  String inputFastqarray_name
  String library_name
  String sequencing_center
  String predictedinsertsize
  String sample_name
  String readgroup
  string comment
  Boolean? seq


  Int? disk_space_gb
  Int? machine_mem_gb
  Int? preemptible_attempts
  String docker
  String gatk_path


  command {
    ${gatk_path} --java-options "-Xmx3000m" \
      FastqToSam \
      --FASTQ ${fastq} \
      --FASTQ2 ${fastq2} \
      --OUTPUT ${readgroup} \
      --PLATFORM ${platform} \
      --LIBRARY_NAME ${library_name} \
      --SAMPLE_NAME ${sample} \
      --SEQUENCING_CENTER ${sequencing_center} \
      --PREDICTED_INSERT_SIZE ${predictedinsertsize}
      --PLATFORM_MODEL=${platform_model} 
      --USE_SEQUENTIAL_FASTQS ${seq} \
      --COMMENT ${comment}
  }
  # revist specs perhaps add bucket
  runtime {
    docker: docker
    memory: select_first([machine_mem_gb, 10]) + " GB"
    cpu: "1"
    disks: "local-disk " + select_first([disk_space_gb, 100]) + " HDD"
    preemptible: select_first([preemptible_attempts, 3])
  }
  output {
    File output_bam = "${readgroup}.unmapped.bam"
  }
}

task CreateUbamList {
  Array[String] unmapped_bams
  String ubam_list_name
  
  Int? machine_mem_gb
  Int? disk_space_gb
  Int? preemptible_attempts
  String docker
  
  command {
    echo "${sep=',' unmapped_bams}" | sed s/"\""//g | sed s/"\["//g | sed s/\]//g | sed s/" "//g | sed 's/,/\n/g' >> ${ubam_list_name}.unmapped_bams.list
    
  }
  output {
    File unmapped_bam_list = "${ubam_list_name}.unmapped_bams.list"   
  }
  runtime {
    docker: docker
    memory: select_first([machine_mem_gb,5]) + " GB"
    cpu: "1"
    disks: "local-disk " + select_first([disk_space_gb, 10]) + " HDD"
    preemptible: select_first([preemptible_attempts, 3])   
    } 
  }
