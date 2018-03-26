#!/usr/bin/env python

import glob
import csv
import os
import argparse
from build_meta import *


def tsvbuild(path, pattern, list_of_paths, tsv_name):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching pattern and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        path: string, path name, either absolute or relative accepted,
              recursively searched
        pattern: string pattern being searched
        tsv_name: filename or tsv file
        list_of_paths: list of strings, containing location of desired values
                       in nested dictionary

    Returns:
        tsv file with format preceded by list_of_paths followed by files
    Notes:
        format of column separation marked by semicolons
        SampleName; output; predictedinsertsize; readgroup; library_name;
        platformmodel; platform; sequencingcenter; Fastq1 ; Fastq2
    """
    exp_dict = {}
    with open('tsv_name.tsv', 'w+') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
        for files in grouper(glob.iglob(path, pattern, recursive=True), 2):
            path, filename_1 = os.path.split(files[0])
            filename_2 = os.path.split(files[1])[1]
            exp_id = filename_1.split('_')[0]
            exp_id_2 = filename_2.split('_')[0]
            if exp_id == exp_id_2:
                exp_dict, metadata = build_metadata(exp_id, path, list_of_paths, input_dict=exp_dict)
                metadata.extend(files)
                # tsv_fileformat:SampleName;output;predictedinsertsize;readgroup
                # library_name;platformmodel;platform;sequencingcenter
                # Fastq1;Fastq2;
                writer.writerow(metadata)
            else:
                # think about break if this is the case
                with open('ubamlog', 'w+') as logfile:
                    logfile.write('{0} and {1} are not paired files \n'.format(exp_id, exp_id_2))
                break
    return tsv_name


# path, pattern, list_of_paths, tsv_name)

def parse_args():
    """Parses arguments
    Args:
    Returns:
        arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='location of parent folder')
    parser.add_argument('pattern', help='location of parent folder')
    parser.add_argument('lists_of_paths', type=list, help='location of parent folder')
    parser.add_argument('tsv_name', help='location of parent folder')
    args = parser.parse_args()
    return (args.path, args.pattern, args.list_of_paths, args.tsv_name)


if __name__ == '__main__':
    input_args = parse_args()
    tsvbuild(*input_args)
