import unittest
from tsvconv import gcloudstorage


class TestUrvMethods(unittest.TestCase):
    """Establish testing environment
    """

    @classmethod
    def setUpClass(cls):
        """Provides gcs account credentials to all tests
        """
        gcloudstorage.set_gcs_env('/root/Hail_Genomic.json')


def main():
    unittest.main()
