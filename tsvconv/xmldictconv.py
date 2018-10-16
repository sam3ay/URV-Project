import xmltodict
from collections import OrderedDict


def xmldictconv(xml_name):
    """Convert xml fie to an ordered dictionary

    Args:
        xml_name (obj): xml file object

    Returns:
        Dictionary version of xml file or empty dictionary if file not found
    """
    try:
        output_dict = xmltodict.parse(xml_name)
        return output_dict
    except OSError:
        return OrderedDict()
