from tsvconv import gcloudstorage
from tsvconv.test import base
from google.datalab import storage


class TestGCSbucket(base.TestUrvMethods):
    """Test bucket related methods
    """

    def testbucketexist(self):
        """
        """
        storage_bucket = gcloudstorage.get_gcsbucket(
                'urv_genetics', '/root/Hail_Genomic.json')
        # Check type
        self.assertIsInstance(
                storage_bucket, storage.Bucket, msg='Object is not a bucket')
        # check if bucket exists
        self.assertTrue(storage_bucket.exists(), msg='Bucket does not Exist')
    
    def testbucketaccess(self):
        """
        """
        blob_bucket = gcloudstorage.blob_generator(
                'urv_genetics', '/root/Hail_Genomic.json')
        self.assertIsInstance(blob_bucket.next(), storage.Object msg='No access to bucket')


if __name__ == '__main__':
    """
    """
    base.main()
