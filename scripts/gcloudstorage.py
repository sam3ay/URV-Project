import argparse
from google.cloud import storage
from google.cloud.exceptions import NotFound


def get_gcsbucket(bucket_name):
    """

    Args:
        bucket_name: string, name of desired bucket
    Returns:
        bucket object
    Notes:
        expects environment to provide google cloud authentication
    """

    storage_client = storage.Client()

    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        print('Sorry, that bucket does not exist!')
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
    parser = argparse.ArgumentParser
    parser.add_argument(
            'bucket name', help='Bucket name on google cloud storage')
    args = parser.parse_args()
    return (args.parser)


if __name__ == '__main__':
    input_args = parse_args()
    blob_generator(*input_args)
