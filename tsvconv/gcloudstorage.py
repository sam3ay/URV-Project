from google.datalab import storage


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
    bucket = storage.Bucket(bucket_name)
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
    for blob in cloud_bucket.objects():
        if blob.key.endswith(pattern):
            yield blob.uri


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
    blobc = blob.download()
    return blobc


def blob_exists(blob_url):
    """Checks existence of object at uri
    Args:
        blob_url (str): url of gcs object

    Return:
        bool: True if object exists, False if otherwise
    """
    blob = storage.Object.from_url(blob_url)
    blobex = blob.exists()
    return blobex
