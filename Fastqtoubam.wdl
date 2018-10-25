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
  String ubam_list_name

  String gatk_docker = "us.gcr.io/broad-gatk/gatk:latest"
  String gatk_path = "/gatk/gatk"
  String work_platform = "illumina"


  # run multiple fastq pair conversions in parallel
  scatter (i in range(length(inputFastqarray))) {
    # Convert pair of FASTQs to uBAM
    call FastqToSam {
      input:
        fastq1=inputFastqarray[i][0],
        fastq2=inputFastqarray[i][1],
        platform=work_platform,
        sequencing_center=inputFastqarray[i][4],
        sample_name=inputFastqarray[i][10],
        readgroup=inputFastqarray[i][5],
        comment=inputFastqarray[i][15],
        library_name=inputFastqarray[i][19],
        predictedinsertsize=inputFastqarray[i][23],
        platform_model=inputFastqarray[i][34],
        docker=gatk_docker,
        gatk_path=gatk_path
    }
  }

# Create a list with the generated ubams
  call CreateUbamList {
     input:
       unmapped_bams = FastqToSam.output_bam,
       ubam_list = ubam_list_name,
       docker = gatk_docker
   }
# Outputs that will be retained when execution is complete
    output {
      Array[File] output_bams = FastqToSam.output_bam
      File ubam_list = CreateUbamList.unmapped_bam_list
    }
}


# TASK DEFINITION


# Convert Fastq files to uBAMs 
task FastqToSam {
  File fastq1
  File fastq2
  String platform
  String platform_model
  String library_name
  String sequencing_center
  String predictedinsertsize
  String sample_name
  String readgroup
  String comment


  String docker
  String gatk_path


  command <<<
    ${gatk_path} --java-options "-Xmx3000m" \
    FastqToSam \
      --FASTQ ${fastq1} \
      --FASTQ2 ${fastq2} \
      --OUTPUT ${readgroup}.unmapped.bam \
      --PLATFORM ${platform} \
      --LIBRARY_NAME "${library_name}" \
      --SAMPLE_NAME ${sample_name} \
      --SEQUENCING_CENTER ${sequencing_center} \
      --PREDICTED_INSERT_SIZE ${predictedinsertsize} \
      --PLATFORM_MODEL ${platform_model} \
      --READ_GROUP_NAME ${readgroup} \
      --COMMENT ${comment} 
  >>>
  # revist specs perhaps add bucket
  runtime {
    docker: docker
    memory: 20 + " GB"
    cpu: "1"
    disks: "local-disk " + 300 + " HDD"
    preemptible: 3
  }
  output {
    File output_bam = "${readgroup}.unmapped.bam"
  }
}

task CreateUbamList {
  Array[String] unmapped_bams
  String ubam_list
  
  String docker
  
  command {
    mv ${write_lines(unmapped_bams)} ${ubam_list}.list
  }
  output {
    File unmapped_bam_list = "${ubam_list}.list"

  }
  runtime {
    docker: docker
    preemptible: 3   
    } 
  }
