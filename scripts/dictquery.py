import functools


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
