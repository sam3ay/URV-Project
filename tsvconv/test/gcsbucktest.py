from tsvconv import gcloudstorage
from tsvconv.test import base
from google.datalab import storage
from google.datalab.utils import RequestException


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
        # check failed permission error handling
        self.assertRaises(
                RequestException,
                gcloudstorage.get_gcsbucket('we', '/root/Hail_Genomic.json'),
                msg='Failed to catch incorrect perimission')

    def testbucketobject(self):
        """
        """
        blob_bucket = gcloudstorage.blob_generator(
                'urv_genetics', '/root/Hail_Genomic.json')
        blob_str = next(blob_bucket)
        self.assertEqual(blob_str[0:5],
                         'gs://',
                         msg='Failed to return google cloud storage link')


if __name__ == '__main__':
    """
    """
    base.main()
