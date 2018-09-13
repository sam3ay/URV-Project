import unittest
from tsvconv import env
import os


class TestGcsStorage(unittest.TestCase):
    """Test gcloudstorage methods
    """

    def test_env(self):
        """Ensure credentials have read only access to the bucket
        """
        env.set_env(
                "GOOGLE_APPLICATION_CREDENTIALS",
                '/root/Hail_Genomic.json')
        self.assertTrue(
                "GOOGLE_APPLICATION_CREDENTIALS" in os.environ,
                msg="Setting Environmental value failed")
        self.assertEqual(
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
                '/root/Hail_Genomic.json',
                msg='Incorrect value for environmental value')
        env.unset_env(
                "GOOGLE_APPLICATION_CREDENTIALS")
        self.assertTrue(
                "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ,
                msg='Unexpected environmental value encountered')


if __name__ == '__main__':
    unittest.main()
