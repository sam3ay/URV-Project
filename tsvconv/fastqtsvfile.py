#!/usr/bin/env python

import glob
import csv
import os
import build_meta
import chunkiter
import argproc


def tsvbuild(gcs, pattern, list_of_paths, tsv_name):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching pattern and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        gcs (str): google cloud bucket name, recursively searched
        pattern (str): file identifying pattern being searched
        tsv_name (str): filename or tsv file
        list_of_paths (list): containing location of desired values
            in nested dictionary

    Returns:
        str: location of tsv file with format preceded by list_of_paths followed by files
    Notes:
        format of column separation marked by semicolons
        SampleName; output; predictedinsertsize; readgroup; library_name;
        platformmodel; platform; sequencingcenter; Fastq1 ; Fastq2
    """
    exp_dict = {}
    with open('tsv_name.tsv', 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
        # glob searches directories while grouper pulls matches two at a time
        for files in chunkiter.grouper(
                glob.iglob(gcs, pattern, recursive=True), 2):
            path, filename_1 = os.path.split(files[0])
            filename_2 = os.path.split(files[1])[1]
            exp_id = filename_1.split('_')[0]
            exp_id_2 = filename_2.split('_')[0]
            if exp_id == exp_id_2:
                exp_dict, metadata = build_meta.build_metadata(
                        exp_id, path, list_of_paths, input_dict=exp_dict)
                metadata.extend(files)
                # tsv_fileformat:SampleName;output;predictedinsertsize;readgroup
                # library_name;platformmodel;platform;sequencingcenter
                # Fastq1;Fastq2;
                writer.writerow(metadata)
            else:
                # think about break if this is the case
                with open('ubamlog', 'w+') as logfile:
                    logfile.write('{0} and {1} are not paired files \n'.format(
                        exp_id, exp_id_2))
                break
    return tsv_name

def tsvbuild(json_path, gcs_bucket, pattern, list_of_paths, tsv_name):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching pattern and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        json_path (str): path to service account json
        gcs (str): google cloud bucket name, recursively searched
        pattern (str): file identifying pattern being searched
        tsv_name (str): filename or tsv file
        list_of_paths (list): containing location of desired values

     Returns:
        str: location of tsv file with format preceded by list_of_paths followed by files
           in nested dictionary
    """



if __name__ == '__main__':
    darg = argproc.parse_args()
    tsvbuild(darg[gcs], darg[pattern], darg[metadata], darg[tsv_name])
