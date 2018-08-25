import unittest
from tsvconv import dict_extract, dictquery
import xmltodict


class TestDictExtract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(
                '/root/URV-Project/tsvconv/test/ERA013549.experiment.xml', 'r'
                ) as xml_file:
            cls.xmldict = xmltodict.parse(xml_file.read())

    def test_gen_dict_extract(self):
        input_dict = next(
                dict_extract.dict_extract('ERX007307', self.xmldict), None)
        fail_dict = next(
                dict_extract.dict_extract('nonsense', self.xmldict), None)
        self.assertEqual(
                input_dict['IDENTIFIERS']['PRIMARY_ID'],
                'ERX007307',
                msg='Failed to extract expected dictionary')
        self.assertEqual(
                fail_dict,
                None,
                msg='Failed None condition')

    def test_dictquery(self):
        input_dict = {'hello': {'all': {'we': {'see': 'there'}}}}
        self.assertEqual(
                dictquery.dictquery(
                    input_dict,
                    ['hello/all/we/see']),
                ['there'],
                msg='Dictionary Parsing error: Unexpected value returned')
        self.assertEqual(
                dictquery.dictquery(
                    input_dict,
                    ['hello/all/nokey/']),
                [None],
                msg='Dictionary Parsing error: TypeError not handled')
        self.assertEqual(
                dictquery.dictquery(
                    input_dict,
                    ['hello/all/we/see/there/attr']),
                [None],
                msg='Dictionary Parsing error: AttributeError not handled')


if __name__ == '__main__':
    unittest.TestCase
