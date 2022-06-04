# from dotenv import load_dotenv
# from weather import weather
# import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt
from colour import Color


def main():
    # Fetch weather data from Met Office for Arts Arkade
    # load_dotenv()
    # weather.get_weather('51.61845146102782', '-3.9425287137489864')

    # Generate Hilbert curve segments
    n = 2
    p = 7  # above p = 7, render time takes ages due to enormous list sizes
    hilbert_curve = HilbertCurve(p, n)
    distances = list(range(2**(p*n)))  # todo refactor with numpy arrays
    points = hilbert_curve.points_from_distances(distances)  # returns Iterable of [x, y] lists of length 'distances'

    # Generate colour range
    start_colour = Color("#006655")  # hard coded here, but could be taken from a dict linking e.g temps to colours
    end_colour = Color("#0000DD")
    colour_range = list(start_colour.range_to(end_colour, len(distances)))  # todo refactor with numpy arrays

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
            plt.plot(xpoints, ypoints, c=str(colour_range[count]))
            count += 1
        except IndexError:
            break

    plt.show()


if __name__ == '__main__':
    main()
