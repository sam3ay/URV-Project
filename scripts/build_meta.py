from dict_extract import *
from dictquery import *
from xmldictconv import *
import os


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
