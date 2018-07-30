from google.cloud import storage
from google.cloud import exceptions as gcsexcept


def gcsauth(json_path):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path (str): Path to service account json
    Returns:
        obj: Service account credentials
    """
    credentials = storage.Client.from_service_account_json(json_path)
    return credentials


def get_gcsbucket(bucket_name, storage_client=storage.Client()):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name (str): name of desired bucket
        storage_client (:obj: optional):Google Cloud account credentials,
            Defaults to environmental variable.
    Returns:
        bucket object
    Notes:
        expects environment to provide google cloud authentication
    """
    try:
        bucket = storage_client.get_bucket(bucket_name)
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
