from google.oauth2client import service_account
from google.datalab import storage
from datalab import context


def gcsauth(json_path):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path (str): Path to service account json
    Returns:
        obj: Service account credentials
    """
    scope = 'https://www.googleapis.com/auth/devstorage.read_only'
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
        storage_client (:obj: optional):Google Cloud account credentials,
            Defaults to environmental variable.
    Returns:
        bucket object
    Raises:
    Notes:
        expects environment to provide google cloud authentication
    """
    credentials = gcsauth(json_path)
    proj_context = get_context(credentials)
    try:
        bucket = storage.Bucket(bucket_name, context=proj_context)
    except gcsexcept.NotFound:
        print('Sorry, that bucket does not exist!')
    except gcsexcept.Forbidden:
        print('Insufficient account permissionsm')
    return bucket


def blob_generator(bucket_name, prefix=None, delimiter='/'):
    """
    WIP
    """
    cloud_bucket = get_gcsbucket(bucket_name)
    for item in cloud_bucket.list_blobs(max_results=20):
        yield item
