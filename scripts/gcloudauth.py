from google.cloud import storage

def googlestorage(bucket_name, ):
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
        bucket = client.get_bucket(bucket_name)
    except:
        print('Sorry, that bucket does not exist!')

    return bucket

