import asyncio


async def dict_endpoints(input_dict, endpoint_dict, key=None):
    """Retrieve key and value pair and yields them as tuples
    Args:
        input_dict (dict): Dictionary with desired values
        endpoint_dict (dict)

    Yields:
        Adds key, value pairs to endpoint_dict
    Example:
        asyncio.run(dict_endpoints(input_dict))
    """
    try:
        for k, v in input_dict.items():
            await dict_endpoints(v, endpoint_dict, key=k)
    except AttributeError:
        if isinstance(input_dict, list):
            for item in input_dict:
                await dict_endpoints(item, endpoint_dict, key=key)
        elif key not in endpoint_dict:
            endpoint_dict[key] = input_dict
        else:
            key += '_2'
            endpoint_dict[key] = input_dict
