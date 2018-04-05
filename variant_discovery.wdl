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
  Array[File] bam_info = read_tsv(bamtsv)
  File ref_fasta
  File known_variants

  Boolean? is_host_aligned
  String? google_apiKey 

  String gatk_docker
  Int? disk_space_gb
  Int? machine_mem_gb
  Int? preemptible_attempts
  String? sparkurl
  String gatk_path

  scatter (bamfile in bam_info) {
    call ReadsPipelineSpark {
      input:
        input_bam = bamfile[0]
        ref_fasta=ref_fasta
        known_variants=known_variants
        gatk_docker=gatk_docker
        output = bamfile[1]

# uBams to vcf
task ReadsPipelineSpark {

  # Inputs for this task
  File input_bam
  File ref_fasta
  File known_variants
  
  Boolean? is_host_aligned
  String? google_apiKey
  
  String gatk_docker

  # You may have to change the following two parameter values depending on the task requirements
  Int default_ram_mb = 208000
  # WARNING: In the workflow, you should calculate the disk space as an input to this task (disk_space_gb).
  Int default_disk_space_gb = 400
  # Mem is in units of GB but our command and memory runtime values are in MB
  Int machine_mem = if defined(mem_gb) then mem_gb *1000 else default_ram_mb
  Int command_mem = machine_mem - 4000
  
  command <<<
    set -e
    export GATK_LOCAL_JAR=${default="/root/gatk.jar" gatk4_jar_override}
      gatk -- java-options "-Xmx${command_mem}m" \
      ReadsPipelineSpark \
      --input ${input_bam}
      --knownSites ${known_variants}
      --output ${output}
      --reference ${ref_fasta}
      --apiKey ${google_apiKey}
      --sparkMaster ${sparkurl}
  >>>
  runtime {
    docker: gatk_docker
    memory: machine_men + " MB"
    disks: "local-disk " + select_first([disk_space_gb, default_disk_space_gb]) + " HDD"
    preemptible: select_first([preemptible_attempts, 3])
    cpu: select_first([cpu, 32])
  }
  output {
  File bam_output = "${sample_name}.bam"
