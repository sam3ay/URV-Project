import unittest
from tsvconv import dict_extract, dictquery
import xmltodict
import asyncio


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
        input_dict = {'hello': {'all': {'we': {'see': 'there'}}},
                      'maybe': {'there': 'will'},
                      'second': {'point': {'there': 'is'}}}
        output_dict = {}
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
                dictquery.dict_endpoints(input_dict, output_dict))
        loop.close()
        self.assertEqual(output_dict['see'],
                         'there',
                         msg='Unexpected endpoint assigned')
        self.assertEqual(output_dict['there'],
                         'will',
                         msg='Unexpected value list check failed')
        self.assertEqual(output_dict['there_2'],
                         'is',
                         msg='Unexpected value list check failed')


if __name__ == '__main__':
    unittest.TestCase
