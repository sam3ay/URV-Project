from tsvconv import argproc
import unittest


class TestArgParse(unittest.TestCase):
    def setUp(self):
        self.parser = argproc.create_parser()

    def test_parserargs(self):
        parser_2 = self.parser.parse_args(
                ['test', 'hello', 'next', 'week', 'there'])
        parse_dict = vars(parser_2)
        self.assertTrue(parse_dict['gcs'])


if __name__ == '__main__':
    unittest.main()
