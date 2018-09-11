from functools import reduce
import asyncio


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


async def dict_endpoints(input_dict, endpoint_dict, key=None):
    """Retrieve key and value pair and yields them as tuples
    Args:
        input_dict (dict): Dictionary with desired values
        endpoint_dict (dict)
        key (str: optional): default key

    Yields:
        tuple of key value
    Example:
        asyncio.run(dict_endpoints(input_dict))
    """
    for k, v in input_dict.items():
        if isinstance(v, dict):
            await dict_endpoints(v, endpoint_dict, key=k)
        else:
            if k in endpoint_dict:
                new_key = '_'.join([key, k])
                endpoint_dict[new_key] = v
            else:
                endpoint_dict[k] = v
