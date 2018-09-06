from tsvconv import argproc
import unittest


class TestArgParse(unittest.TestCase):
    def setUp(self):
        self.parser = argproc.create_parser()

    def test_parserargs(self):
        parser_2 = self.parser.parse_args(
                ['test', 'hello', 'next', 'week', 'there'])
        parse_dict = vars(parser_2)
        self.assertEqual(parse_dict['gcs'], 'test')
        self.assertEqual(parse_dict['suffix'], 'hello')
        self.assertEqual(parse_dict['tsv_name'], 'next')
        self.assertEqual(parse_dict['json'], 'week')
        self.assertEqual(parse_dict['metadata'], 'there')


if __name__ == '__main__':
    unittest.main()
