import unittest
from tsvconv import xmldictconv
import xmltodict


class XmlToDictTest(unittest.TestCase):
    """

    """

    def test_xmltodict(self):
        """
        """
        with open('test.xml', 'r') as testxml:
            self.assertEqual(
                    xmldictconv.xmldictconv(testxml.read())
                    , xmltodict.parse(testxml.read()),
                    msg='Dictionary Conversion Error')
