from google.oauth2client import service_account
from google.datalab import storage
from datalab import context
from google.datalab.utils import RequestException


def gcsauth(json_path,
            scope='https://www.googleapis.com/auth/devstorage.read_only'):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path (str): Path to service account json

    Returns:
        obj: Service account credentials
    """
    credentials = service_account.Credentials.from_service_account_file(
            json_path, scopes=(scope,))
    return credentials


def get_context(credentials):
    """Initializes a context object

    Args:
        credentials (obj): Google Cloud account authorization.

    Returns:
        Context object.  Used for connecting with Google Cloud APIs.
    """
    context_obj = context.Context(credentials.project_id, credentials)
    return context_obj


def get_gcsbucket(bucket_name, json_path):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name (str): name of desired bucket
        json_path (str): Path to service account json

    Returns:
        bucket object

    Raises:
        RequestException: If the bucket does not exist or
            the service_account has inadequate permissions

    Notes:
        expects environment to provide google cloud authentication
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
    """
    cloud_bucket = get_gcsbucket(bucket_name, json_path)
    for blob in cloud_bucket.objects():
        if blob.key.endswith(pattern):
            yield blob.uri
