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
                'urv_genetics')
        # Check type
        self.assertIsInstance(
                storage_bucket, storage.Bucket, msg='Object is not a bucket')
        # check if bucket exists
        self.assertTrue(
                storage_bucket.exists(),
                msg='Bucket does not Exist')
        with self.assertRaises(
                IsADirectoryError,
                msg='Directory Error not handled'):
            gcloudstorage.set_gcs_env('/root/')
            gcloudstorage.get_gcsbucket('urv_genetics')
        with self.assertRaises(
                gcloudstorage.DefaultCredentialsError,
                msg='Failed to identify non json file'):
            gcloudstorage.set_gcs_env('/root/bad')
            gcloudstorage.get_gcsbucket('urv_genetics')
        with self.assertRaises(
                AttributeError,
                msg='Failed to identify incorrect json file'):
            gcloudstorage.set_gcs_env('/root/rand.json')
            gcloudstorage.get_gcsbucket('urv_genetics')
        with self.assertRaises(
                gcloudstorage.DefaultCredentialsError,
                msg='Found non existing json file'):
            gcloudstorage.set_gcs_env('/root/noexist')
            gcloudstorage.get_gcsbucket('urv_genetics')

    def testbucketobject(self):
        """
        """
        gcloudstorage.set_gcs_env('/root/Hail_Genomic.json')
        blob_bucket = gcloudstorage.blob_generator(
                'urv_genetics')
        blob_str = next(blob_bucket)
        self.assertEqual(
                blob_str[0:5],
                'gs://',
                msg='Failed to return google cloud storage link')
        with self.assertRaises(
                RequestException,
                msg="Bucket Doesn't exist"):
            next(gcloudstorage.blob_generator('defidfdfjsdi'))
        with self.assertRaises(
                RequestException,
                msg="Failed to identify Insffucient Permission"):
            next(gcloudstorage.blob_generator('where'))


if __name__ == '__main__':
    """
    """
    base.main()
