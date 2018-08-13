def gen_dict_extract(value, var, des_dict=None):
    """Search a list of nested dictionaries

    Args:
        value(obj): Object being searched for
        var(iterable): iterable containing dictionaries or lists
        des_dict(dict): Dictionary being traversed

    Yields:
        Dictionary containing desired values
    """
    # not optimal
    try:
        for k, v in var.items():
            if v == value:
                yield des_dict
            # lists should be caugt by the except
            elif isinstance(v, (dict, list)):
                for result in gen_dict_extract(value, v, des_dict):
                    yield result
    except AttributeError:
        if isinstance(var, list):
            for d in var:
                des_dict = d
                for result in gen_dict_extract(value, d, des_dict):
                    yield result
