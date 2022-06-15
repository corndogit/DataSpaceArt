import os
from dotenv import load_dotenv
# from weather import get_weather
import colourpalette as cpt
from datetime import datetime
import numpy as np
import json
from hilbertcurve.hilbertcurve import HilbertCurve
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from colour import Color


def main(config):
    # Separate config.json
    curve_config = config["hilbertCurveProperties"]
    weather_config = config['weatherDataProperties']

    load_dotenv()  # dev tool: replaces config.json keys with env keys
    if os.environ["DATAHUB_API_KEY"] and os.environ["DATAHUB_SECRET"]:
        weather_config["dataHubAPIKey"] = os.getenv("DATAHUB_API_KEY")
        weather_config["dataHubSecret"] = os.getenv("DATAHUB_SECRET")

    # Fetch weather data from Met Office DataHub API
    # input_data: dict = get_weather(weather_config)

    # Generate Hilbert curve segments
    n = 2
    # p = cpt.get_p_from_windspeed(input_data['WindSpeed'])
    p = cpt.get_p_from_windspeed(5)
    hilbert_curve = HilbertCurve(p, n)
    distances = np.arange(2**(p*n))
    points = np.asarray(hilbert_curve.points_from_distances(distances))

    # Generate colour range (line)
    # start_line_colour = Color(cpt.line_temperature(round(input_data["MaxTemperature"])))
    # end_line_colour = Color(cpt.line_temperature(round(input_data["MinTemperature"])))
    start_line_colour = Color(cpt.line_temperature(19))
    end_line_colour = Color(cpt.line_temperature(12))
    line_colour_range = np.fromiter(start_line_colour.range_to(end_line_colour, len(distances)),
                                    dtype='S16',
                                    count=len(distances))

    # Generate colormap (background)
    # bg_colormap = ListedColormap(cpt.bg_color_list(input_data['SignificantWeatherCode']))
    bg_colormap = ListedColormap(cpt.bg_color_list('2'))

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
    linewidth = 2 * (7 / p)
    for p in range(len(points)):
        try:
            start, end = points[p], points[p + 1]
            xpoints = (start[0], end[0])
            ypoints = (start[1], end[1])
            plt.plot(xpoints, ypoints,
                     color=str(line_colour_range[p], encoding='utf-8'),
                     linewidth=linewidth)
        except IndexError:
            break

    # apply background colormap
    # bg_shape = cpt.bg_direction(input_data["WindDirection"])
    bg_shape = cpt.bg_direction(112)
    ax.imshow(bg_shape,
              cmap=bg_colormap,
              interpolation='bicubic',
              extent=plt.xlim() + plt.ylim(), vmin=0, vmax=1)

    # save figure to file
    if curve_config["saveFigToFile"]:
        if not os.path.exists('../generated_figures/'):
            os.makedirs('../generated_figures/')
        filename = datetime.now()
        file_format: str = curve_config["outputFormat"].lower()  # allowed formats: png, svg, pdf
        plt.savefig(f"../generated_figures/fig-{filename.strftime('%d%m%Y_%H%M%S')}.{file_format}",
                    format=file_format,
                    pad_inches=0)


if __name__ == '__main__':
    with open('../config.json') as config_file:
        main(json.load(config_file))

    plt.show()
