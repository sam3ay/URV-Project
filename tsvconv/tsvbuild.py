#!/usr/bin/env python

import csv
import argproc
import dict_extract
import dictquery
import gcloudstorage
import xmldictconv
import env
import pathhandling
import asyncio


def tsvbuild(
        json_path, gcsbucket, suffix, pairflag,
        tsv_name, default, metaflag):
    """builds a tsv file from a directory of paired files

    Retrieves location of pairs of files matching suffix and retrieves
    metadata information from the parent directory located in an xml file
    Assumes paired files differences occur after an underscore '_'.

    Args:
        json_path (str): path to the json credentials file for GCS access
        gcsbucket (str): google cloud bucket name, recursively searched
        suffix (str): file identifying pattern being searched
        tsv_name (str): filename or tsv file
        default (bool): Use the default credentials
        metaflag (bool): Find and write metadata
        pairflag (bool): Find and write File pair

    Returns:
        str: location of tsv file
    Notes:
        format of column separation marked by tabs
        SampleName; output; predictedinsertsize; readgroup; library_name;
        platformmodel; platform; sequencingcenter; Fastq1 ; Fastq2

    Dev:
        Add dictquery to list of links
    """
    exp_dict = {}
    # set google auth
    if not default:
        env.set_env(
            'GOOGLE_APPLICATION_CREDENTIALS',
            json_path)
    header = True
    loop = asyncio.get_event_loop()
    for gcs_url in gcloudstorage.blob_generator(gcsbucket, suffix):
        meta_dict = {}
        meta_dict['File'] = gcs_url
        if pairflag:
            gcs_pairname, gcs_pairpath, accension = pathhandling.get_fileurl(
                    url=gcs_url,
                    sep=suffix[0],
                    suffix=suffix,
                    depth=0,
                    pair=pairflag)
            if gcloudstorage.blob_exists(gcs_pairpath):
                meta_dict['File_2'] = gcs_pairpath
        else:
            # seeking to create a filename
            gcs_fileout, gcs_filepath, parent = pathhandling.get_fileurl(
                    url=gcs_url,
                    sep=suffix[0],
                    suffix=suffix,
                    depth=0,
                    pair=True)
            meta_dict['output'] = gcs_fileout
        if metaflag:
            exp_name, exp_path, exp_folder = pathhandling.get_fileurl(
                    url=gcs_url,
                    sep=suffix[0],
                    suffix='.experiment.xml',
                    depth=1,
                    pair=False)
            try:
                curr_dict = next(dict_extract.dict_extract(
                        value=accension,
                        var=exp_dict[exp_name]))
            except KeyError:
                xmlfile = gcloudstorage.blob_download(exp_path)
                exp_dict[exp_name] = xmldictconv.xmldictconv(xmlfile)
                curr_dict = next(dict_extract.dict_extract(
                        value=accension,
                        var=exp_dict[exp_name]))
            loop.run_until_complete(
                    dictquery.dict_endpoints(
                        input_dict=curr_dict,
                        endpoint_dict=meta_dict))
        tsvwriter(tsv_name, meta_dict, header)
        header = False
    loop.close()
    if not default:
        env.unset_env('GOOGLE_APPLICATION_CREDENTIALS')
    return tsv_name


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
            tsv_name=darg['tsv_name'],
            default=darg['default'],
            pairflag=darg['pairflag'],
            metaflag=darg['metaflag'])
