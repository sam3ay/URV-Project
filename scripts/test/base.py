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


if __name__ == '__main__':
    """
    """
    unittest.main()
