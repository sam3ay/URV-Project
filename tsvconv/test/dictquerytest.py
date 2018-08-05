import unittest
from tsvconv import dictquery


class DictQueryTest(unittest.TestCase):
    """

    """

    def test_dictquery(self):
        """

        """
        input_dict = {'hello': {'all': {'we': {'see': 'there'}}}}
        self.assertEqual(dictquery.dictquery(input_dict, [
            'hello/all/we/see']), ['there'], msg='Dictionary Parsing error')
