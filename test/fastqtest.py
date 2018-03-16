import unittest
from fastqtsvfile import *
import xmltodict


class TestFastqTsvMethods(unittest.TestCase):
    """
    
    """

    def test_xmltodict(self):
        """

        """
        with open('test.xml', 'r') as testxml:
            self.assertEqual(xmldictconv('test.xml'), xmltodict.parse(testxml.read()))

    def test_gen_dict_extract(self):
        """

        """
        input_dict = {'hello':{'all':{'we':{'see':[{'Hold':'up'}, {'Regardless':'if'}]}}}}
        self.assertEqual([x for x in gen_dict_extract('up', input_dict)], [{'Hold':'up'}])

    def test_grouper(self):
        """
        """
        self.assertEqual([x for x in grouper(range(2), 2)], [(0, 1)])

    def test_dictquery(self):
        """
        """
        input_dict = {'hello': {'all': {'we': {'see': 'there'}}}}
        self.assertEqual(dictquery(input_dict, ['hello/all/we/see']), ['there'])

if __name__ == '__main__':
    """
    
    """
    unittest.main()
