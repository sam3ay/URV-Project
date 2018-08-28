from google.auth.exceptions import DefaultCredentialsError
from google.datalab import storage
from google.datalab.utils import RequestException
from json.decoder import JSONDecodeError


def get_gcsbucket(bucket_name):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name (str): name of desired bucket

    Returns:
        bucket object

    Raises:
        RequestException: The service_account has inadequate permissions
        DefaultCredentialsError: Environment json file not found or
            Error parsing Json File
        IsADirectoryError: When directory supplied instead of file
        AttributeError: Not a valid service_account.Credentials object
    """
    try:
        bucket = storage.Bucket(bucket_name)
    except RequestException:
        raise
    except DefaultCredentialsError:
        raise
    except IsADirectoryError:
        raise
    except AttributeError:
        raise
    return bucket


def blob_generator(bucket_name, pattern):
    """Yields blob object url location

    Args:
        bucket_name (str): name of desired bucket
        pattern (str): unique characters and extension desired files contain

    Yields:
        Link to Google Cloud storage object
    Raises:
        RequestException: Bucket doesn't exist
    """
    cloud_bucket = get_gcsbucket(bucket_name)
    try:
        for blob in cloud_bucket.objects():
            if blob.key.endswith(pattern):
                yield blob.uri
    except RequestException:
        raise


def blob_download(blob_url):
    """Retrieves content of google cloud object
    Args:
        blob_url (str): url of gcs object

    Return:
        Content of GCS object
    Raises:
        TypeError: Non-bytes like Object Retrieved;
            Indicative of non existing key
    """
    blob = storage.Object.from_url(blob_url)
    try:
        blobc = blob.download()
    except TypeError:
        raise
    return blobc
