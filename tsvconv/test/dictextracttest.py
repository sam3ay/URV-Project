import unittest
from tsvconv import dict_extract
import xmltodict


class TestDictExtract(unittest.TestCase):
    def test_gen_dict_extract(self):
        with open('/root/URV-Project/tsvconv/test/ERA013549.experiment.xml', 'r') as xml_file:
            xmldict = xmltodict.parse(xml_file.read())
        input_dict = next(dict_extract.dict_extract('ERX007307', xmldict), None)
        fail_dict = next(dict_extract.dict_extract('nonsense', xmldict), None)
        self.assertEqual(
                input_dict['IDENTIFIERS']['PRIMARY_ID'],
                'ERX007307',
                msg='Failed to extract expected dictionary')
        self.assertEqual(
                fail_dict,
                None,
                msg='Failed None condition')


if __name__ == '__main__':
    unittest.TestCase
