#!/usr/bin/env python

import csv
import os
from tsvconv import build_meta
from tsvconv import chunkiter
from tsvconv import argproc
from tsvconv import dict_extract
from tsvconv import dictquery
from tsvconv import gcloudstorage
from tsvconv import xmldictconv


def tsvbuild(json_path, gcs, pattern, list_of_paths, tsv_name):
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
        str: location of tsv file
    Notes:
        format of column separation marked by semicolons
        SampleName; output; predictedinsertsize; readgroup; library_name;
        platformmodel; platform; sequencingcenter; Fastq1 ; Fastq2

    Dev:
        Add dictquery to list of links
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


def dictbuild(keys, values):
    """builds a dictionary

    Retrieves location of pairs of files matching pattern and retrieves
    metadata information from an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        keys (list): list of keys of size n
        values (list): list of values of size n

    Returns:
        dict: dictionary
    Raises:
        ValueError: If lenght of keys and values are unequal
    """
    if len(keys) == len(values):
        output_dict = dict(zip(keys, values))
    else:
        raise ValueError("Unexpected input")
    return output_dict


def tsvwriter(filepath, input_dict):
    """Write dictionary contents to tsv file
    Args:
        filepath (str): absolute path to location of file
        input_dict (dict): field names as keys and values
            as a list of elements in that field name row
    """
    try:
        with open(filepath, 'a') as tsvfile:
            fieldnames = input_dict.keys()
            writer = csv.DictWriter(
                    tsvfile,
                    fieldnames=fieldnames,
                    dialect='excel-tab')
            writer.writerow(input_dict)
    except IOError:
        with open(filepath, 'a+') as tsvfile:
            fieldnames = input_dict.keys()
            writer = csv.DictWriter(
                    tsvfile,
                    fieldnames=fieldnames,
                    dialect='excel-tab')
            writer.writeheader()
            writer.writerow(input_dict)
    except IsADirectoryError:
        raise


if __name__ == '__main__':
    darg = argproc.parse_args()
    tsvbuild(darg[gcs], darg[pattern], darg[metadata], darg[tsv_name])
