from colour import Color
from math import floor
import numpy as np
import weathercodes


def get_p_from_windspeed(windspeed: float or int):
    """Returns a value for the order of the Hilbert curve from natural log of the wind speed.

     Ranges from 3 to 8 for the sake of keeping the pattern interesting when the wind is low,
     and to prevent huge memory usage caused with a value beyond 8.
     """
    MIN_ORDER = 3
    MAX_ORDER = 8
    if windspeed == 0:
        return MIN_ORDER
    p = floor(np.log(windspeed) + 2)
    return min(max(p, MIN_ORDER), MAX_ORDER)


def line_temperature(temperature: int):
    """Finds a colour hex value for a specific temperature, returns a string."""
    MIN_TEMP = -10
    MAX_TEMP = 35
    colours = list(Color('#11e').range_to('#e11', MAX_TEMP - MIN_TEMP + 1))  # + 1 to prevent IndexError
    if temperature < MIN_TEMP:
        return '#cc0199'  # magenta
    elif temperature > MAX_TEMP:
        return '#69020b'  # dark red
    else:
        for k, v in enumerate(colours, MIN_TEMP):
            if temperature == k:
                return str(v)


def bg_color_list(weathercode: str):
    """Returns a list of RGB values to use with ListedColormap"""
    COLORMAP_LENGTH = 512
    colours = weathercodes.code_to_colours[weathercode]
    start_bg_colour = Color(colours[0])
    return [colr.rgb for colr in list(start_bg_colour.range_to(colours[1], COLORMAP_LENGTH))]


def bg_direction(direction: int):
    """Calculates a direction to begin gradient from. Converts bearing to an 8-way compass direction, and
    returns a corresponding 3x3 scalar image to use with plt.imshow().

    1 is added to inter-cardinal positions and 1.5 is added to cardinals, as this provides a more complete
    colour gradient for the cardinal positions in practice.
    """
    shape = np.zeros((3, 3))
    coords = {
        'N': (0, 1),
        'NE': (0, 2),
        'E': (1, 2),
        'SE': (2, 2),
        'S': (2, 1),
        'SW': (2, 0),
        'W': (1, 0),
        'NW': (0, 0)
    }
    directions = [k for k in coords.keys()]
    idx = directions[floor((direction / 45) % 8)]
    if idx in ['N', 'E', 'S', 'W']:
        shape[coords[idx]] += 1.5
    else:
        shape[coords[idx]] += 1
    return shape


if __name__ == '__main__':
    print("get_p_from_windspeed(windspeed: float or int)\n22mph wind = ", get_p_from_windspeed(22))
    print("line_temperature(temperature: int)\n22C = ", line_temperature(22))
    print(f"bg_color_list(weathercode: str)\nSignificant Weather Code 1 = {bg_color_list('1')[0:8]}...")
    print("bg_direction(direction: int) with Bearing 220 = \n", bg_direction(220))
