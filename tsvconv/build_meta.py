from tsvconv import dict_extract
from tsvconv import dictquery
from tsvconv import xmldictconv
import os


def build_metadata(input_dict, xmlpath, list_of_paths):
    """Generates metadata from xml file

    Args:
        input_dict (string): Name of the dictionary from which information
                    will be extracted
        xmlfile (obj): string, location of xml file
        input_dict (dict): optional variable, dictionary,
                    contains metadata information
    Returns:
        list of strings, metadata information
    Notes:
        'DESIGN/SAMPLE_DESCRIPTOR/PRIMARY_ID',
        'DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME,
        'PLATFORM/ILLUMINA/INSTRUMENTAL_MODEL', ILLUMINA, SC
    """
    # retrieve parent directory from xmlfile and specify experiment xml file
    exp_loc = os.xmlfile.absxmlfile(os.xmlfile.join(xmlfile, os.pardir))
    exp_id = os.xmlfile.split(exp_loc)[1]
    exp_name = exp_loc + os.sep + exp_id + '.experiment.xml'
    try:
        experiment = next(
                dict_extract.gen_dict_extract(
                    input_dict, input_dict[exp_name]), None)
    except KeyError:
        input_dict[exp_name] = xmldictconv.xmldictconv(exp_name)
        experiment = next(
                dict_extract.gen_dict_extract(
                    input_dict, input_dict[exp_name]), None)
    return (input_dict, dictquery.dictquery(experiment, list_of_xmlfiles))
