from google.auth.exceptions import DefaultCredentialsError
from google.datalab import storage
from google.datalab.utils import RequestException
from json.decoder import JSONDecodeError
import os


def set_gcs_env(json_path):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path (str): Path to service account json

    Returns:
        Environmental variable providing service account credentials
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path


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


def blob_generator(bucket_name, pattern='_1.fastq.bz2'):
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
