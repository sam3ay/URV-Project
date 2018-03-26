import itertools


def grouper(iterable, size, fillvalue=None):
    """Fetches elements from an iterable at the specified size at a time

    Args:
        iterable: traversable object
        size: Integer, specifies size of slice
        fillvalue: Integer or String symbol to fill missing chunk space.

    Returns:
        tuple, chunk of an iterable of specified size
    """
    chunk = [iter(iterable)] * size
    return itertools.zip_longest(*chunk, fillvalue=fillvalue)
