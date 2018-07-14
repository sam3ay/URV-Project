import unittest
import xmltodict


class XmlToDictTest(unittest.TestCase):
    """

    """

    def test_xmltodict(self):
        """

        """
        with open('test.xml', 'r') as testxml:
            self.assertEqual(
                    xmltodict.xmldictconv(
                        'test.xml'), xmltodict.parse(testxml.read()))

