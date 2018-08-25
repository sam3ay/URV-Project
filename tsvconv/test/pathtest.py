from tsvconv import pathhandling
import unittest


class TestParseUrl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = ('gs://urv_genetics/ftp.ddbj.nig.ac.jp/'
                   'ddbj_database/dra/fastq/ERA013/'
                   'ERA013549/ERX007307/ERR018783_1.fastq.bz2')

    def testgetparentfile(self):
        filename = None
        sep = '.'
        fileext = 'experiment.xml'
        depth = 1
        parentfile = pathhandling.get_fileurl(
                self.url,
                filename,
                sep,
                fileext,
                depth)
        parenturl = ('gs://urv_genetics/ftp.ddbj.nig.ac.jp/'
                     'ddbj_database/dra/fastq/ERA013/'
                     'ERA013549/ERA013549.experiment.xml')

        self.assertEqual(
                parentfile[1],
                parenturl,
                msg='Unexpected Unnamed Parent File returned')
        self.assertEqual(
                pathhandling.get_fileurl(
                    'is/it/me/where',
                    'hello',
                    sep,
                    fileext,
                    depth)[1],
                'is/it/hello.experiment.xml',
                msg='Unexpected Parent File returned')
        with self.assertRaises(
               IndexError,
                msg='Out of Index request not handled'):
            filename = None
            fileext = 'Nope'
            depth = 5
            parentfile = pathhandling.get_fileurl(
                    'no/parent',
                    filename,
                    sep,
                    fileext,
                    depth)

    def testgetpairfile(self):
        filename = None
        filesep = '_'
        fileext = '2.fastq.bz2'
        depth = 0
        pairfile = pathhandling.get_fileurl(
                self.url,
                filename,
                filesep,
                fileext,
                depth,
                pair=True)
        pairurl = ('gs://urv_genetics/ftp.ddbj.nig.ac.jp/'
                   'ddbj_database/dra/fastq/ERA013/'
                   'ERA013549/ERX007307/ERR018783_2.fastq.bz2')
        self.assertEqual(
                pairfile[1],
                pairurl,
                msg='Not a pair file')
        self.assertEqual(
                pathhandling.get_fileurl(
                    'hello/where/are/we.here',
                    'they',
                    '_',
                    'there',
                    0,
                    pair=True)[1],
                'hello/where/are/they_there')
