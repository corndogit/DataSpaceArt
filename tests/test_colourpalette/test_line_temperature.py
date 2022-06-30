import unittest
from DataSpaceArt_main.colourpalette import line_temperature


class TestLineTemperature(unittest.TestCase):
    def test_below_min_temp(self):
        result = line_temperature(-25)
        self.assertEqual(result, '#cc0199')

    def test_above_max_temp(self):
        result = line_temperature(50)
        self.assertEqual(result, '#69020b')

    def test_realistic_temp(self):
        result = line_temperature(20)
        self.assertEqual(result, '#a4ee11')


if __name__ == '__main__':
    unittest.main()
