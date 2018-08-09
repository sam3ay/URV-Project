import unittest
from tsvconv import gcloudstorage
from google.oauth2 import service_account
from datalab import context


class TestGcsAuthentication(unittest.TestCase):
    """Test gcloudstorage methods
    """

    def test_credentials(self):
        """Ensure credentials have read only access to the bucket
        """
        credentials = gcloudstorage.gcsauth('/root/Hail_Genomic.json')
        scopes = ('https://www.googleapis.com/auth/devstorage.read_only',)
        self.assertIsInstance(
                credentials,
                service_account.Credentials, msg='Not credential class')
        self.assertEqual(
                credentials.scopes, scopes, msg='Incorrect Permissions')
        self.assertRaises(
                IsADirectoryError,
                gcloudstorage.gcsauth('/root/'),
                msg='Directory Error not handled')
        self.assertRaises(
                gcloudstorage.JSONDecodeError,
                gcloudstorage.gcsauth('/root/bad'),
                msg='Failed to identify non json file')
        self.assertRaises(
                AttributeError,
                gcloudstorage.gcsauth('/root/rand.json'),
                msg='Failed to identify incorrect json file')

    def test_context(self):
        """Ensure context is set
        """
        credentials = service_account.Credentials.from_service_account_file(
                '/root/Hail_Genomic.json')
        context_c = gcloudstorage.get_context(credentials)
        # check type
        self.assertIsInstance(
                context_c, context.Context, msg='Not context class')


if __name__ == '__main__':
    unittest.main()
