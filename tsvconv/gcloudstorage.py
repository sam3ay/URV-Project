from google.oauth2 import service_account
from google.datalab import storage
from datalab import context
from google.datalab.utils import RequestException
from json.decoder import JSONDecodeError


def gcsauth(json_path,
            scope='https://www.googleapis.com/auth/devstorage.read_only'):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path (str): Path to service account json

    Returns:
        obj: Service account credentials

    Raises:
        JSONDecodeError: When file can't be decoded
        IsADirectoryError: When directory supplied instead of file
        AttributeError: Unexpected Json file provided
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
                json_path, scopes=(scope,))
    except IsADirectoryError:
        raise
    except JSONDecodeError:
        raise
    except AttributeError:
        raise
    return credentials


def get_context(credentials):
    """Initializes a context object

    Args:
        credentials (obj): Google Cloud account authorization.

    Returns:
        Context object.  Used for connecting with Google Cloud APIs.
    Raise:
        AttributeError: Not a valid service_account.Credentials object
    """
    try:
        context_obj = context.Context(credentials.project_id, credentials)
    except AttributeError:
        raise
    return context_obj


def get_gcsbucket(bucket_name, json_path):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name (str): name of desired bucket
        json_path (str): Path to service account json

    Returns:
        bucket object

    Raises:
        RequestException: The service_account has inadequate permissions
    """
    credentials = gcsauth(json_path)
    proj_context = get_context(credentials)
    try:
        bucket = storage.Bucket(bucket_name, context=proj_context)
    except RequestException:
        raise
    return bucket


def blob_generator(bucket_name, json_path, pattern='_1.fastq.bz2'):
    """Yields blob object url location

    Args:
        bucket_name (str): name of desired bucket
        json_path (str): Path to service account json

    Yields:
        Link to Google Cloud storage object
    Raises:
        RequestException: Bucket doesn't exist
    """
    cloud_bucket = get_gcsbucket(bucket_name, json_path)
    try:
        for blob in cloud_bucket.objects():
            if blob.key.endswith(pattern):
                yield blob.uri
    except RequestException:
        raise
