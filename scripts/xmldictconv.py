import xmltodict


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
