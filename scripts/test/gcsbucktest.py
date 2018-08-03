import base
import gcloudstorage


class TestGCSbucket(base.TestUrvMethods):
    """Test bucket related methods
    """

    def Testbucket(self):
        """
        """
        storage_bucket = gcloudstorage.get_gcsbucket(
                'bucket name', '~/Hail_Genomic.json')
        # Check type
        # check if bucket exists
        self.assertTrue(storage_bucket.exists(), msg='Bucket does not Exist')
        # Check access to bucket
