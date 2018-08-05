import base
import gcloudstorage
from google.datalab import storage
import unittest


class TestGCSbucket(base.TestUrvMethods):
    """Test bucket related methods
    """

    def Testbucket(self):
        """
        """
        storage_bucket = gcloudstorage.get_gcsbucket(
                'bucket name', '/root/Hail_Genomic.json')
        # Check type
        self.assertIsInstance(
                storage_bucket, storage.Bucket, msg='Object is not a bucket')
        # check if bucket exists
        self.assertTrue(storage_bucket.exists(), msg='Bucket does not Exist')
        # Check access to bucket
        self.assertIsInstance(
                storage_bucket.metadata, msg='No access to storage_bucket')


if __name__ == '__main__':
    unittest.main()
