#!/usr/bin/env python

import csv
import argproc
import dict_extract
import dictquery
import gcloudstorage
import xmldictconv
import env
import pathhandling


def tsvbuild(json_path, gcsbucket, pattern, list_of_paths, tsv_name):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching pattern and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        json_path (str): path to the json credentials file for GCS access
        gcsbucket (str): google cloud bucket name, recursively searched
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
    meta_key = ['fastq1', 'fastq2'] + list_of_paths
    # set google auth
    env.set_env(
        'GOOGLE_APPLICATION_CREDENTIALS',
        json_path)
    for gcs_url in gcloudstorage.blob_generator(gcsbucket, pattern):
        exp_name, exp_path = pathhandling.get_fileurl(
                url=gcs_url,
                filename=None,
                sep='.',
                suffix='experiment.xml',
                path=1)
        gcs_pairname, gcs_pairpath = pathhandling.get_fileurl(
                url=gcs_url,
                filename=None,
                sep='_',
                suffix='2.Fastq.bz2',
                depth=0,
                pair=True)
        output_bam = 'gs://{0}/output/{1}.bam'.format(gcsbucket, gcs_pairname)
        metalist = [gcs_url, gcs_pairpath, output_bam]
        try:
            metadata = dictquery.dictquery(
                    input_dict=exp_dict[exp_name],
                    listofpath=list_of_paths)
        except KeyError:
            xmlfile = gcloudstorage.blob_download(exp_path, gcsbucket)
            xml_dict = xmldictconv(xmlfile)
            exp_dict[exp_name] = dict_extract.dict_extract(
                    value=gcs_pairname,
                    var=xml_dict)
            metadata = dictquery.dictquery(
                    input_dict=exp_dict[exp_name],
                    listofpath=list_of_paths)
        metalist += metadata
        meta_dict = dictbuild(
                key=meta_key,
                value=metalist)
        tsvwriter(tsv_name, meta_dict)
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
    parser = argproc.create_parser()
    args = parser.parse_args()
    darg = vars(args)
    tsvbuild(
            json_path=darg['json'],
            gcsbucket=darg['gcs'],
            pattern=darg['pattern'],
            list_of_paths=darg['metadata'],
            tsv_name=darg['tsv_name'])
