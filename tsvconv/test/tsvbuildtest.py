from tsvconv import tsvbuild
from tsvconv.test import base
import magic


class TestTsvBuild(base.TestUrvMethods):

    def testdictbuild(self):
        keys = ['foo', 'bar', 'hello', 'why', 'is', 'there']
        values = [0, 1, 2, 3, 4, 5]
        wrong_size_list = [0, 1, 3]
        pass_dict = tsvbuild.dictbuild(keys, values)
        key_check = 'foo'
        exp_val = 2
        self.assertIsInstance(
                pass_dict,
                dict,
                msg='Is not a dictionary'
                )
        self.assertTrue(
                key_check in pass_dict,
                msg="Key Error: key doesn't exist in dictionary")
        self.assertEqual(
                pass_dict['hello'],
                exp_val,
                msg="Unexpected value returned")
        self.assertEqual(
                pass_dict.keys(),
                keys,
                msg="Unexpected key order")
        with self.assertRaises(
                ValueError,
                msg="Incorrect list size accepted"):
            tsvbuild.dictbuild(keys, wrong_size_list)

    def testtsvwriter(self):
        input_dict = {'foo': 'where', 'bar': 'there'}
        file_test = '/root/URV-Project/tsv_test.tsv'
        tsvfile_test = tsvbuild.tsvwriter(file_test, input_dict)
        file_control = open('/root/URV-Project/tsv_expected', 'w')
        directory_file = '/root/'
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
        with self.assertRaises(
                IsADirectoryError,
                msg='Failed to identify directory instead of file'):
            tsvbuild.tsvwriter(directory_file, input_dict)
