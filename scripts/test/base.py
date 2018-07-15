import unittest
from google.cloud import storage


class TestUrvMethods(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        Creates temporary directory
        Provides gcs account credentials to all tests
        """
        storage_client = storage.Client.from_service_account_json(
                'project_service_account.json')

    def tearDown(self):
        """
        """
    def bucketexist(self):
        """
        """


if __name__ == '__main__':
    """
    """
    unittest.main()
