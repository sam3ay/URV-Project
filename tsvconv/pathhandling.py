from pathlib import PurePath
from urllib import parse


def get_fileurl(url, filename, sep, suffix, depth, pair=False):
    """Retrieve path of file with specified file name and extension

    Args:
        url (str): Path being scanned
        filename (str): Name of file or folder
        sep (str): character separating file and extension
        suffix (str): extension of file or folder in parent directory.
        depth (int): Which ancestor the file is located in
        pair (bool, optional): Flag, if True, looks for pair of input file

    Returns:
        str: path to file or folder in parent
    Raises:
        IndexError: If depth is greater than amount of ancestors
    Notes:
        suffix = os.sep, returns a folder path instead of a file
    """
    urlp = parse.urlparse(url)
    path = urlp.path
    accension = None
    try:
        parentpath = PurePath(path).parents[depth]
    except IndexError:
        raise
    if filename is None and pair:
        filename = PurePath(path).parts[-1].split(sep)[0]
        accension = PurePath(path).parts[-2]
    elif filename is None:
        filename = parentpath.parts[-1]
    if suffix is not None:
        filereturn = filename + sep + suffix
    else:
        filereturn = filename
    output_path = parentpath.joinpath(filereturn)
    output_url = parse.urlunparse(
            (urlp.scheme,
             urlp.netloc,
             output_path.as_posix(),
             urlp.params,
             urlp.query,
             urlp.fragment)
            )
    return (filename, output_url, accension)
