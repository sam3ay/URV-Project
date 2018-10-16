from tsvconv import gcloudstorage
from tsvconv.test import base
from google.datalab import storage


class TestGCSbucket(base.TestUrvMethods):
    """Test bucket related methods
    """

    def testbucketexist(self):
        storage_bucket = gcloudstorage.get_gcsbucket(
                'urv_genetics')
        # Check type
        self.assertIsInstance(
                storage_bucket, storage.Bucket, msg='Object is not a bucket')
        # check if bucket exists
        self.assertTrue(
                storage_bucket.exists(),
                msg='Bucket does not Exist')

    def testbloblink(self):
        blob_bucket = gcloudstorage.bloblink_generator(
                'urv_genetics', '/root/Hail_Genomic.json')
        blob_str = next(blob_bucket)
        self.assertEqual(
                blob_str[0:5],
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

    def testblobexists(self):
        blob_true = "gs://urv_genetics/output/ERR018779_1.fastq"
        blob_false = "gs://urv_genetics/output/what"
        self.assertTrue(gcloudstorage.blob_exists(blob_true),
                        msg="Failed to identify existing blob")
        self.assertFalse(gcloudstorage.blob_exists(blob_false),
                         msg="Failed to identify nonexisting blob")


if __name__ == '__main__':
    base.main()
