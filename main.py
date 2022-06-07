import os
from dotenv import load_dotenv
# from weatherlib import weather
from datetime import datetime
import numpy as np
import json
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt
from colour import Color


def main(config):
    # Separate config.json
    curve_config = config["hilbertCurveProperties"]
    weather_config = config['weatherDataProperties']

    load_dotenv()  # dev tool: replaces config.json keys with env keys
    if os.environ["DATAHUB_API_KEY"] and os.environ["DATAHUB_SECRET"]:
        weather_config["dataHubAPIKey"] = os.getenv("DATAHUB_API_KEY")
        weather_config["dataHubSecret"] = os.getenv("DATAHUB_SECRET")

    # Fetch weather data from Met Office for Arts Arkade
    # weather.get_weather(weather_config)

    # Generate Hilbert curve segments
    n = 2
    p = 3  # warning: this increases the number of points (and memory requirements) exponentially!!
    hilbert_curve = HilbertCurve(p, n)
    distances = np.arange(2**(p*n))
    full_distance = len(distances)
    points = np.asarray(hilbert_curve.points_from_distances(distances))  # returns ndarray of [x, y] points of length 'distances'

    # Generate colour range
    start_colour = Color("red")  # hard coded here, but could be taken from a dict linking e.g temps to colours
    end_colour = Color("#5522FF")
    colour_range = np.fromiter(start_colour.range_to(end_colour, full_distance), dtype='S16', count=full_distance)

    # Configure subplot, background formatting
    # | Removes all axis labels, forces 1:1 aspect ratio, sets size
    px = 1 / curve_config["displayDPI"]
    fig = plt.figure(figsize=(1000 * px, 1000 * px), dpi=curve_config["displayDPI"])
    ax = fig.add_subplot()
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('#333333')  # todo use weather data to change figure bg colour
    plt.tick_params(left=False,
                    bottom=False,
                    labelleft=False,
                    labelbottom=False)
    for side in ['top', 'left', 'bottom', 'right']:
        ax.spines[side].set_visible(False)

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

    if curve_config["saveFigToFile"]:
        filename = datetime.now()
        file_format: str = curve_config["outputFormat"]  # allowed formats: png, svg, pdf
        plt.savefig(f"generated_figures/fig-{filename.strftime('%d%m%Y_%H%M%S')}.{file_format}",
                    format=file_format,
                    bbox_inches='tight',
                    pad_inches=0)


if __name__ == '__main__':
    with open('config.json') as config_file:
        main(json.load(config_file))

    plt.show()
