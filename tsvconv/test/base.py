import unittest
from tsvconv import env


class TestUrvMethods(unittest.TestCase):
    """Establish testing environment
    """

    @classmethod
    def setUpClass(cls):
        """Provides gcs account credentials to all tests
        """
        env.set_env(
                'GOOGLE_APPLICATION_CREDENTIALS',
                '/root/Hail_Genomic.json')


def main():
    unittest.main()
