from colour import Color
from math import floor
import numpy as np


def get_p_from_windspeed(windspeed):
    if windspeed == 0:
        return 3
    p = floor(np.log(windspeed) + 2)
    return min(max(p, 3), 8)


def line_temperature(temperature: int):
    min_temp = -10
    max_temp = 35
    colours = list(Color('#11e').range_to('#e11', max_temp - min_temp + 1))
    if temperature < min_temp:
        return '#cc0199'  # magenta
    elif temperature > max_temp:
        return '#69020b'  # dark red
    else:
        for k, v in enumerate(colours, min_temp):
            if temperature == k:
                return str(v)


def bg_direction(direction):
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
    temp = input("Please specify a temperature:\n")
    print(f"{temp} corresponds to value {line_temperature(int(temp))}")
