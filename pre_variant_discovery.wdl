## Based on Broad Institutes GATK4 best preactices
## Requirements/expectations:
## - Pair-end sequencing data in unmapped FASTQ
## - Input FASTQ Requirements
## -- filenames all have the same suffix (we use ".fastq.gz")
## -- files must pass validation by ValidateSamFile
## -- reads are provided in query-sorted order
## -- all reads must have an RG tag
## Output :
## - A clean BAM file and its index, suitable for variant discovery analyses.
##
## Software version requirements (see recommended dockers in inuts JSON)
## - GATK4.beta.3 or later
## - Samtools (see gotc docker)
## - Python 2.7
##
## Cromwell version support 
## - Successfully tested on v28 
## - Does not work on versions < v23 due to output syntax

# Workflow Definition
workflow PreProcessingForVariantDiscovery_GATK4 {

  String sample_name
  String ref_fasta_name
  
  File flowcell_fastq_list
  String fastq_suffix

  File ref_fasta
  File ref_fasta_index
  File ref_dict

  String bwa_commandline
  Int compression_level

  File dbSNP_vcf
  File dbSNP_vcf_index
  Array[File] known_indels_sites_VCFs
  Array[File] known_indels_sites_indices

  String gotc_docker
  String pickard_docker 
  String gatk_docker
  String python_docker



