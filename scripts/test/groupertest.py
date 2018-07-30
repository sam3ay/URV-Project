import unittest
import chunkiter


class ChunkIterTest(unittest.TestCase):
    """
    
    """

    def test_grouper(self):
        """

        """
        self.assertEqual([x for x in chunkiter.grouper(range(2), 2)], [(0, 1)])
