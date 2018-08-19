from tsvconv import dict_extract
from tsvconv import dictquery
from tsvconv import xmldictconv
import os


def build_metadata(identifier, path, list_of_paths, input_dict={}):
    """Generates metadata from xml file

    Args:
        identifier: string, Name of the dictionary from which information
                    will be extracted
        path: string, location of xml file
        input_dict: optional variable, dictionary,
                    contains metadata information
    Returns:
        list of strings, metadata information
    Notes:
        'DESIGN/SAMPLE_DESCRIPTOR/PRIMARY_ID',
        'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME,
        'PLATFORM/ILLUMINA/INSTRUMENTAL_MODEL', ILLUMINA, SC
    """
    # retrieve parent directory from path and specify experiment xml file
    exp_loc = os.path.abspath(os.path.join(path, os.pardir))
    exp_id = os.path.split(exp_loc)[1]
    exp_name = exp_loc + os.sep + exp_id + '.experiment.xml'
    try:
        experiment = next(
                dict_extract.gen_dict_extract(
                    identifier, input_dict[exp_name]), None)
    except KeyError:
        input_dict[exp_name] = xmldictconv.xmldictconv(exp_name)
        experiment = next(
                dict_extract.gen_dict_extract(
                    identifier, input_dict[exp_name]), None)
    return (input_dict, dictquery.dictquery(experiment, list_of_paths))
