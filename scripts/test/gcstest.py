import base
import gcloudstorage


class TestGcsMethods(base.TestUrvMethods):
    """Test gcloudstorage methods
    """

    def test_scopes(self):
        """Ensure credentials have read only access to the bucket
        """
        credentials = gcloudstorage.gcsauth('~/Hail_Genomic.json')
        scopes = 'https://www.googleapis.com/auth/devstorage.read_only'
        self.assertEqual(credentials.scope, scopes)
