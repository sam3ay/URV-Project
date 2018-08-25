from google.auth.exceptions import DefaultCredentialsError
from google.datalab import storage
from google.datalab.utils import RequestException
from json.decoder import JSONDecodeError


def get_gcsbucket(bucket_name):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name (str): name of desired bucket
        json_path (str): Path to service account json

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


def bloblink_generator(bucket_name, json_path, pattern='_1.fastq.bz2'):
    """Yields blob object url location

    Args:
        bucket_name (str): name of desired bucket
        json_path (str): Path to service account json

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

    def blob_download(blob_key, bucket_name, json_path):
        """Retrieves content of google cloud object
        Args:
            blob_key (str): key of gcs object
            bucket_name (str): name of desired bucket
            json_path (str): Path to service account json

        Return:
            Content of GCS object
        Raises:
            TypeError: Non-bytes like Object Retrieved;
                Indicative of non existing key
        """
        bucket = get_gcsbucket(bucket_name, json_path)
        blob = bucket.object(blob_key)
        try:
            blobc = blob.download()
        except TypeError:
            raise
        return blobc
