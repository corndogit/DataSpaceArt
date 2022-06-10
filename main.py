import os
from dotenv import load_dotenv
# from weatherlib import weather
from datetime import datetime
import numpy as np
import json
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from colour import Color


def generate_colour_range(start: Color, end: Color, length: int):
    """Takes two Color objects and generates a colour range, returns a numpy array of colour bytestrings"""
    return np.fromiter(start.range_to(end, length), dtype='S16', count=length)


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
    points = np.asarray(hilbert_curve.points_from_distances(distances))  # returns ndarray of [x, y] points of length 'distances'

    # Generate colour range (line)
    start_line_colour = Color("red")
    end_line_colour = Color("#5522FF")

    line_colour_range = generate_colour_range(start_line_colour, end_line_colour, len(distances))

    # Generate colormap (background)
    start_bg_colour = Color("#333333")
    end_bg_colour = Color("#E4E4E4")
    bg_colormap = ListedColormap([colr.rgb for colr in list(start_bg_colour.range_to(end_bg_colour, 128))])

    # Configure subplot, background formatting
    # | Removes all axis labels, forces 1:1 aspect ratio, sets size
    px = 1 / curve_config["displayDPI"]
    sizes = curve_config["imageDimensions"]
    fig = plt.figure(figsize=(sizes["width"] * px, sizes["height"] * px),
                     dpi=curve_config["displayDPI"])
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    ax = fig.add_subplot()
    ax.set_aspect('auto', adjustable='box')
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
            plt.plot(xpoints, ypoints,
                     color=str(line_colour_range[count], encoding='utf-8'),
                     linewidth=2)  # another factor that can be changed by data
            count += 1
        except IndexError:
            break

    # apply background colormap
    ax.imshow([[0, 0], [1, 1]],
              cmap=bg_colormap,
              interpolation='bicubic',
              extent=plt.xlim() + plt.ylim(), vmin=0, vmax=1)

    if curve_config["saveFigToFile"]:
        if not os.path.exists('/generated_figures/'):
            os.makedirs('/generated_figures/')
        filename = datetime.now()
        file_format: str = curve_config["outputFormat"].lower()  # allowed formats: png, svg, pdf
        plt.savefig(f"generated_figures/fig-{filename.strftime('%d%m%Y_%H%M%S')}.{file_format}",
                    format=file_format,
                    pad_inches=0)


if __name__ == '__main__':
    with open('config.json') as config_file:
        main(json.load(config_file))

    plt.show()
