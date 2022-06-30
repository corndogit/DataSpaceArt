import unittest
from DataSpaceArt_main.colourpalette import bg_direction


class TestBgDirection(unittest.TestCase):
    def setUp(self):
        """Taken from the coords dictionary inside bg_direction()"""
        self.south_pattern = (2, 1)
        self.northeast_pattern = (0, 2)

    def tearDown(self):
        pass

    def test_direction_cardinal(self):
        result = bg_direction(180)
        self.assertEqual(result[self.south_pattern], 1.5)

    def test_direction_intercardinal(self):
        result = bg_direction(45)
        self.assertEqual(result[self.northeast_pattern], 1)


if __name__ == '__main__':
    unittest.main()
