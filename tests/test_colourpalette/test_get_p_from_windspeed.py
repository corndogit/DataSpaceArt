import unittest
from DataSpaceArt_main.colourpalette import get_p_from_windspeed


class TestGetPFromWindspeed(unittest.TestCase):
    def test_low_wind_speed(self):
        result = get_p_from_windspeed(2.391283)
        self.assertEqual(result, 3)

    def test_extreme_high_wind_speed(self):
        result = get_p_from_windspeed(500)
        self.assertEqual(result, 8)

    def test_realistic_wind_speed(self):
        result = get_p_from_windspeed(32.1232143)
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
