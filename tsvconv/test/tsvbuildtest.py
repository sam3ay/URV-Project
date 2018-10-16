from tsvconv import tsvbuild
from tsvconv.test import base
import magic


class TestTsvBuild(base.TestUrvMethods):

    def testtsvwriter(self):
        input_dict = {'foo': 'where', 'bar': 'there'}
        file_test = '/root/URV-Project/tsv_test.tsv'
        tsvfile_test = tsvbuild.tsvwriter(file_test, input_dict)
        file_control = open('/root/URV-Project/tsv_expected', 'w')
        empty_dict = {}
        self.assertEqual(magic.from_file(
            tsvfile_test),
            "TSV document, Version",
            msg='Output document is not a tsv file')
        self.assertEqual(
                tsvfile_test.read(),
                file_control.read(),
                msg='Test File is different from control file')
        with self.assertRaises(
                ValueError,
                msg='Value Error due to blank field names expected'):
            tsvbuild.tsvwriter(tsvfile_test, empty_dict)
