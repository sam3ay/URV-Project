from tsvconv import gcloudstorage
from tsvconv.test import base
from google.datalab import storage
from google.datalab.utils import RequestException


class TestGCSbucket(base.TestUrvMethods):
    """Test bucket related methods
    """

    def testbucketexist(self):
        storage_bucket = gcloudstorage.get_gcsbucket(
                'urv_genetics', '/root/Hail_Genomic.json')
        # Check type
        self.assertIsInstance(
                storage_bucket, storage.Bucket, msg='Object is not a bucket')
        # check if bucket exists
        self.assertTrue(storage_bucket.exists(), msg='Bucket does not Exist')

    def testbloblink(self):
        blob_bucket = gcloudstorage.bloblink_generator(
                'urv_genetics', '/root/Hail_Genomic.json')
        blob_str = next(blob_bucket)
        self.assertEqual(blob_str[0:5],
                         'gs://',
                         msg='Failed to return google cloud storage link')

    def testblobdownload(self):
        blob = gcloudstorage.blob_download(
                'blob_key',
                'bucket_name',
                'json_path')
        self.assertEqual(
                blob[0:5],
                "b'<?xml",
                msg='Unexpected File Encountered')
        with self.assertRaises(
                TypeError,
                msg='Key not found'):
            gcloudstorage.blob_download(
                    'blob_key', 'bucket_name', 'json_path')


if __name__ == '__main__':
    base.main()
