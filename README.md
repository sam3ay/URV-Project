# Germline analysis pipeline

Workflows used for germline short variant discovery on WGS data following GATK best practices.

## Requirements/expectations
- Directory of Human whole-genome paired-end sequencing data in Fastq format
  - Metadata in xml format in parent directory
  - Input Fastqs are expected to share the same prefix pattern ("123_1", "123_2") 

## Outputs
- uBam
- GVCF(in progress)
- VCF?(in progress)

## ToDo
- Hail tertiary analysis
