from functools import reduce


def dictquery(input_dict, listofpath):
    """Fetches data from nested dictionary
    Args:
        input_dict (dict): Dictionary with desired values
        listofpath (list): path of desired value
    Returns:
        list of values at path specified by input list
    Notes:
        KeyError hidden by nonetype
    """
    output_list = []
    try:
        for path in listofpath:
            output_list.append(
                    reduce(dict.get, path.split('/'), input_dict))
    except TypeError:
        output_list.append(None)
    return output_list
