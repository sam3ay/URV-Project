from functools import reduce


def dictquery(input_dict, listofpath):
    """Fetches data from nested dictionary
    Args:
        input_dict (dict): Dictionary with desired values
        listofpath (list): path of desired value
    Returns:
        list of values at path specified by input list
    Raises:
        TypeError: When key is not in dictionary
        AttributeError: When reduce runs dict.get on non dictionary object
    Notes:
    """
    output_list = []
    try:
        for path in listofpath:
            output_list.append(
                    reduce(dict.get, path.split('/'), input_dict))
    except TypeError:
        output_list.append(None)
    except AttributeError:
        output_list.append(None)
    return output_list
