#!/usr/bin/env python

import glob
import itertools
import csv
import os
import xmltodict
import functools
import argparse

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


def build_metadata(identifier, path, list_of_paths, input_dict={}):
    """Generates metadata from xml file

    Args:
        identifier: string, Name of the dictionary information will be extracted from
        path: string, location of xml file
        input_dict: optional variable, dictionary, contains metadata information
    
    Returns:
        list of strings, metadata information
    Notes:
        'DESIGN/SAMPLE_DESCRIPTOR/PRIMARY_ID',
        'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME,
        'PLATFORM/ILLUMINA/INSTRUMENTAL_MODEL', ILLUMINA, SC
       
    """
    # retrieve parent directory from path and specify experiment xml file
    exper_dict = input_dict
    exp_loc = os.path.abspath(os.path.join(path, os.pardir))
    exp_id = os.path.split(exp_loc)[1]
    exp_name = exp_loc + os.sep + exp_id + '.experiment.xml'
    try:
        experiment = next(gen_dict_extract(identifier, exper_dict[exp_name]), None)
    except KeyError:
        exper_dict[exp_name] = xmldictconv(exp_name)
        experiment = next(gen_dict_extract(identifier, exper_dict[exp_name]), None)
     return (exper_dict, dictquery(experiment, list_of_paths))


def xmldictconv(xml_name):
    """Convert xml fie to an ordered dictionary

    Args:
        xml_name: string, path to xml file

    Returns:
        Dictionary version of xml file or empty dictionary if file not found
    """
    try:
        with open(xml_name, 'r') as xml_file:
            output_dict = xmltodict.parse(xml_file.read())
        return output_dict
    except OSError:
        return {}


def grouper(iterable, size, fillvalue=None):
    """Fetches elements from an iterable at the specified size at a time

    Args:
        iterable: traversable object
        size: Integer, specifies size of slice
        fillvalue: Integer or String symbol to fill missing chunk space.

    Returns:
        tuple, chunk of an iterable of specified size
    """
    chunk = [iter(iterable)] * size
    return itertools.zip_longest(*chunk, fillvalue=fillvalue)


def gen_dict_extract(value, var, des_dict=None):
    """Search a list of nested dictionaries

    Args:
        value: Object being search
        var: iterable containing dictionaries or lists
        des_dict: default dictionary

    Yields:
        Dictionary containing desired values
    """
    # not optimal
    try:
        for k, v in var.items():
            if v == value:
                yield des_dict
    except AttributeError:
        pass
    else:
        # try excepts all the way down?
        if isinstance(v, dict):
            for result in gen_dict_extract(value, v, des_dict):
                yield result
        elif isinstance(v, list):
            for d in v:
                des_dict = d
                for result in gen_dict_extract(value, d, des_dict):
                    yield result


def dictquery(input_dict, listofpath):
    """Fetches data from nested dictionary
    Args:
        input_dict: nested Dictionary
        listofpath: path of desired value
    
    Returns:
        list of values at path specified by input list
    """
    output_list = []
    for path in listofpath:
        output_list.append(functools.reduce(dict.get, path.split('/'), input_dict))
    return output_list

# path, pattern, list_of_paths, tsv_name)

def parse_args():
    """Parses arguments
    Args:
    
    Returns:
        arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=string, help='location of parent folder')
    parser.add_argument('pattern', type=string, help='location of parent folder')
    parser.add_argument('lists_of_paths', type=list, help='location of parent folder')
    parser.add_argument('tsv_name', type=string, help='location of parent folder')
    return (args.path, args.pattern, args.list_of_paths, args.tsv_name)


if __name__ == '__main__':
    input_args = parse_args()
    tsvbuild(*input_args)
