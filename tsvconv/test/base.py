import unittest
from tsvconv import env


class TestUrvMethods(unittest.TestCase):
    """Establish testing environment
    """

    @classmethod
    def setUpClass(cls):
        """Provides gcs account credentials to all tests
        """
        default = True
        if not default:
            env.set_env(
                    'GOOGLE_APPLICATION_CREDENTIALS',
                    '/root/Hail_Genomic.json')

    @classmethod
    def tearDownClass(cls):
        """Removes gcs environmental variable
        """
        try:
            env.unset_env(
                    'GOOGLE_APPLICATION_CREDENTIALS')
        except KeyError:
            print("default credentials used")


def main():
    unittest.main()
