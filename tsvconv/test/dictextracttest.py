import unittest
from tsvconv import dict_extract


class TestDictExtract(unittest.case):
    """
    """

    def test_gen_dict_extract(self):
        input_dict = {
                'hello':
                {'all':
                    {'we': {'see': [{'Hold': 'up'}, {'Regardless': 'if'}]}}}}
        self.assertEqual(
                [x for x in dict_extract.gen_dict_extract(
                    'up', input_dict)], [{'Hold': 'up'}],
                msg='Failed to extract expected dictionary')
