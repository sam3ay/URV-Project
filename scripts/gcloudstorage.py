import argparse
from google.cloud import storage
from google.cloud import exceptions


def gcsauth(json_path):
    """Provides the Google Cloud service account credentials to be used

    Args:
        json_path: string, path to service account json
    Returns:
        Service account credentials
    """
    credentials = storage.Client.from_service_account_json(json_path)
    return credentials


def get_gcsbucket(bucket_name, storage_client=storage.Client()):
    """Retrieves Google Cloud storage bucket

    Args:
        bucket_name: string, name of desired bucket
        storage_client: object, Google Cloud account credentials,
                        Defaults to environmental variable.
    Returns:
        bucket object
    Notes:
        expects environment to provide google cloud authentication
    """
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except exceptions.NotFound:
        print('Sorry, that bucket does not exist!')
    except exceptions.Forbidden:
        print('Insufficient account permissionsm')
    return bucket


def blob_generator(bucket_name, prefix=None, delimiter='/'):
    """
    WIP
    """
    cloud_bucket = get_gcsbucket(bucket_name)
    for item in cloud_bucket.list_blobs(max_results=20):
        yield item


def parse_args():
    """Parses arguments
    Args:
    Returns: arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name',
                        help='Bucket name on google cloud storage')
    parser.add_argument('-j', '--json', help='Path to service account json')
    args = parser.parse_args()
    return (args.parser)


if __name__ == '__main__':
    """
    """
    input_args = parse_args()
    get_gcsbucket(*input_args)
