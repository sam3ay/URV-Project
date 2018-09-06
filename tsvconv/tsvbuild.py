#!/usr/bin/env python

import csv
import argproc
import dict_extract
import dictquery
import gcloudstorage
import xmldictconv
import env
import pathhandling


def tsvbuild(json_path, gcsbucket, suffix, list_of_paths, tsv_name):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching suffix and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        json_path (str): path to the json credentials file for GCS access
        gcsbucket (str): google cloud bucket name, recursively searched
        suffix (str): file identifying pattern being searched
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
    meta_key = ['fastq1', 'fastq2', 'output'] + list_of_paths
    # set google auth
    env.set_env(
        'GOOGLE_APPLICATION_CREDENTIALS',
        json_path)
    header = True
    for gcs_url in gcloudstorage.blob_generator(gcsbucket, suffix):
        exp_name, exp_path, exp_folder = pathhandling.get_fileurl(
                url=gcs_url,
                filename=None,
                sep='.',
                suffix='experiment.xml',
                depth=1,
                pair=False)
        gcs_pairname, gcs_pairpath, accension = pathhandling.get_fileurl(
                url=gcs_url,
                filename=None,
                sep='_',
                suffix='2.Fastq.bz2',
                depth=0,
                pair=True)
        output_bam = 'gs://{0}/output/{1}.ubam'.format(gcsbucket, gcs_pairname)
        metalist = [gcs_url, gcs_pairpath, output_bam]
        try:
            curr_dict = next(dict_extract.dict_extract(
                    value=accension,
                    var=exp_dict[exp_name]))
            metadata = dictquery.dictquery(
                    input_dict=curr_dict,
                    listofpath=list_of_paths)
        except KeyError:
            xmlfile = gcloudstorage.blob_download(exp_path)
            exp_dict[exp_name] = xmldictconv.xmldictconv(xmlfile)
            curr_dict = next(dict_extract.dict_extract(
                    value=accension,
                    var=exp_dict[exp_name]))
            metadata = dictquery.dictquery(
                    input_dict=curr_dict,
                    listofpath=list_of_paths)
        metalist += metadata
        meta_dict = dictbuild(
                keys=meta_key,
                values=metalist)
        tsvwriter(tsv_name, meta_dict, header)
        header = False
    return tsv_name


def dictbuild(keys, values):
    """builds a dictionary

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
        print(keys, values)
        raise ValueError("Unexpected input")
    return output_dict


def tsvwriter(filepath, input_dict, header):
    """Write dictionary contents to tsv file
    Args:
        filepath (str): absolute path to location of file
        input_dict (dict): field names as keys and values
            as a list of elements in that field name row
        header (bool): Flag determing whehter header is written
    """
    with open(filepath, 'a') as tsvfile:
        fieldnames = input_dict.keys()
        writer = csv.DictWriter(
                tsvfile,
                fieldnames=fieldnames,
                dialect='excel-tab')
        if header:
            writer.writeheader()
        writer.writerow(input_dict)


if __name__ == '__main__':
    parser = argproc.create_parser()
    args = parser.parse_args()
    darg = vars(args)
    tsvbuild(
            json_path=darg['json'],
            gcsbucket=darg['gcs'],
            suffix=darg['suffix'],
            list_of_paths=darg['metadata'],
            tsv_name=darg['tsv_name'])
