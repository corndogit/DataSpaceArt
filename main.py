# from dotenv import load_dotenv
# from weatherlib import weather
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt
from colour import Color


def main():
    # Fetch weather data from Met Office for Arts Arkade
    # load_dotenv()
    # weather.get_weather('51.61845146102782', '-3.9425287137489864')

    # Generate Hilbert curve segments
    n = 2
    p = 6  # warning: this increases the number of points (and memory requirements) exponentially!!
    hilbert_curve = HilbertCurve(p, n)
    distances = np.arange(2**(p*n))
    full_distance = len(distances)
    points = np.asarray(hilbert_curve.points_from_distances(distances))  # returns ndarray of [x, y] points of length 'distances'

    # Generate colour range
    start_colour = Color("#006655")  # hard coded here, but could be taken from a dict linking e.g temps to colours
    end_colour = Color("#0000DD")
    colour_range = np.fromiter(start_colour.range_to(end_colour, full_distance), dtype='S8', count=full_distance)

    # Configure subplot, background formatting
    # | Removes all axis labels, forces 1:1 aspect ratio
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('#333333')  # todo use weather data to change figure bg colour
    plt.tick_params(left=False,
                    bottom=False,
                    labelleft=False,
                    labelbottom=False)

    # plot segments
    count = 0
    for _ in points:
        try:
            start, end = points[count], points[count + 1]
            xpoints = (start[0], end[0])
            ypoints = (start[1], end[1])
            plt.plot(xpoints, ypoints, c=str(colour_range[count], encoding='utf-8'))
            count += 1
        except IndexError:
            break

    plt.show()


if __name__ == '__main__':
    main()
