from pathlib import PurePath
from urllib import parse


def get_fileurl(url, filename, sep, fileext, depth, pair=False):
    """Retrieve path of file with specified file name and extension

    Args:
        url (str): Path being scanned
        filename (str): Name of file or folder
        sep (str): character separating file and extension
        fileext (str): extension of file or folder in parent directory.
        depth (int): Which ancestor the file is located in
        pair (bool, optional): Flag, if True, looks for pair of input file

    Returns:
        str: path to file or folder in parent
    Raises:
        IndexError: If depth is greater than amount of ancestors
    Notes:
        fileext = os.sep returns a folder path instead of a file
        When filename is none returns the pair file
    """
    urlp = parse.urlparse(url)
    path = urlp.path
    try:
        parentpath = PurePath(path).parents[depth]
    except IndexError:
        raise
    if filename is None and pair:
        filename = PurePath(path).parts[-1].split(sep)[0]
    elif filename is None:
        filename = parentpath.parts[-1]
    if fileext is not None:
        filename = filename + sep + fileext
    output_path = parentpath.joinpath(filename)
    output_url = parse.urlunparse(
            (urlp.scheme,
             urlp.netloc,
             output_path.as_posix(),
             urlp.params,
             urlp.query,
             urlp.fragment)
            )
    return output_url
