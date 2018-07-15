import unittest
import gstorage


class TestUrvMethods(unittest.TestCase):
    """Establish testing environment
    """

    def setUp(self):
        """
        Provides gcs account credentials to all tests
        Retrieves google bucket
        WIP: Creates temporary directory
        """
        storage_client = gstorage.google_auth('authenticate key')
        storage_bucket = gstorage.get_bucket(storage_client, 'bucket name')


if __name__ == '__main__':
    """
    """
    unittest.main()
