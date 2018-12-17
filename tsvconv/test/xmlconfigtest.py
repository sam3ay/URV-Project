import unittest
from tsvconv import xmlconfigparse
import xml.etree.ElementTree as ET


class XmlToDictTest(unittest.TestCase):
    """

    """
    @classmethod
    def setUpClass(cls):
        """Creates new xml file to test"""
        root = ET.Element('root')
        foo = ET.SubElement(root, 'foo')
        ET.SubElement(foo, 'bar')
        ET.SubElement(foo, 'bar')

        tree = ET.ElementTree(root)
        tree.write("test.xml")

    def test_xmlinsert(self):
        """
        """
        xmlfile = xmlconfigparse.xmlinsert('bar/name(Text)/value(total)',
                                           'test.xml',
                                           tag='foo[last()]'
                                           )
        try:
            xmlroot = ET.parse(xmlfile).getroot()
        except ET.ParseError:
            self.fail(msg="Xml Parse Error")
        xmlteststring = ET.tostring(xmlroot)
        xmltempstring = ("b'<root><foo><bar /><bar /><bar><name>Text<value>"
                         "total</value></name></bar></foo></root>'"
                         )
        self.assertEqual(xmlteststring,
                         xmltempstring,
                         msg="Unexpected string returned"
                         )
