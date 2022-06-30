import unittest
from DataSpaceArt_main.colourpalette import bg_color_list


class TestBGColorList(unittest.TestCase):
    def setUp(self):
        """Some example weather codes which may be returned from the API - refer to weathercodes.py"""
        self.clear = '0'
        self.cloudy = '7'
        self.light_rain = '9'

    def tearDown(self):
        pass

    def test_bg_color_list_clear(self):
        """Check to see if last value in the returned list is an RGB value matching
        the 2nd colour in the weather code tuple"""
        result = bg_color_list(self.clear)
        final_rgb_value = (0.7019607843137255, 0.9725490196078427, 0.9843137254901958)
        self.assertEqual(result[-1], final_rgb_value)

    def test_bg_color_list_cloudy(self):
        result = bg_color_list(self.cloudy)
        final_rgb_value = (0.9490196078431372, 0.9490196078431372, 0.9490196078431372)
        self.assertEqual(result[-1], final_rgb_value)

    def test_bg_color_list_light_rain(self):
        result = bg_color_list(self.light_rain)
        final_rgb_value = (0.7215686274509804, 0.7686274509803923, 0.9372549019607842)
        self.assertEqual(result[-1], final_rgb_value)


if __name__ == '__main__':
    unittest.main()
