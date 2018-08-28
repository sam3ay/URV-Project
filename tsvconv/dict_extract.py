def dict_extract(value, var, ret_dict=None):
    """Search a list of nested dictionaries

    Args:
        value(obj): Object being searched for
        var(iterable): iterable containing dictionaries or lists
        ret_dict(dict): Highest depth dictionary containing value

    Yield:
        Dictionary containing desired values
    Notes:
        Find highest depth dictionary in the lowest depth list
        that contains the desired value
    """
    try:
        for v in var.values():
            if v == value and ret_dict is not None:
                yield ret_dict
            elif v == value and ret_dict is None:
                yield var
            # lists should be caugt by the except
            elif isinstance(v, (dict, list)):
                for result in dict_extract(value, v, ret_dict):
                    yield result
    except AttributeError:
        if isinstance(var, list):
            for d in var:
                ret_dict = d
                for result in dict_extract(value, d, ret_dict):
                    yield result
