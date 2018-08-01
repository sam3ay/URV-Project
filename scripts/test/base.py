import unittest
import gcloudstorage

class TestUrvMethods(unittest.TestCase):
    """Establish testing environment
    """

    @classmethod
    def setUpClass(cls):
        """Provides gcs account credentials to all tests
        """
        credentials = gcloudstorage.gcsauth('~/Hail_Genomic.json')

    def setUp(self):
        """
        Retrieves google bucket
        WIP: Creates temporary directory
        """
        storage_bucket = gstorage.get_bucket(storage_client, 'bucket name')


if __name__ == '__main__':
    """
    """
    unittest.main()
