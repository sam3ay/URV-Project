def gen_dict_extract(value, var, des_dict=None):
    """Search a list of nested dictionaries

    Args:
        value: Object being search
        var: iterable containing dictionaries or lists
        des_dict: default dictionary

    Yields:
        Dictionary containing desired values
    """
    # not optimal
    try:
        for k, v in var.items():
            if v == value:
                yield des_dict
    except AttributeError:
        pass
    else:
        # try excepts all the way down?
        if isinstance(v, dict):
            for result in gen_dict_extract(value, v, des_dict):
                yield result
        elif isinstance(v, list):
            for d in v:
                des_dict = d
                for result in gen_dict_extract(value, d, des_dict):
                    yield result
