from colour import Color
from datetime import datetime
from hilbertcurve.hilbertcurve import HilbertCurve
import io
import os
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import colourpalette as cpt


class HilberCurvePlotter:
    def __init__(self, input_data: dict, curve_config: dict):
        self.input_data = input_data
        self.curve_config = curve_config

    def plot(self):
        self._set_hilbert_curve_properties()
        ax = self._create_axes_instance()

        # plot segments
        linewidth = self.curve_config['baseLinewidth'] * (7 / self.p)
        for p in range(len(self.points)):
            try:
                start, end = self.points[p], self.points[p + 1]
                xpoints = (start[0], end[0])
                ypoints = (start[1], end[1])
                plt.plot(xpoints, ypoints,
                        color=str(self.line_colour_range[p], encoding='utf-8'),
                        linewidth=linewidth)
            except IndexError:
                break

        # apply background colormap
        bg_shape = cpt.bg_direction(self.input_data["WindDirection"])
        ax.imshow(bg_shape,
                cmap=self.bg_colormap,
                interpolation='bicubic',
                extent=plt.xlim() + plt.ylim(),
                vmin=0,
                vmax=1)

    def save(self):
        img_bytes = io.BytesIO()
        file_format: str = self.curve_config["outputFormat"].lower()  # allowed formats: png, svg, pdf
        plt.savefig(img_bytes,
                    format=file_format,
                    pad_inches=0)

        img = Image.open(img_bytes)
        if self.curve_config['showFigImage']:
            img.show()

        filename = datetime.now().strftime('%d%m%Y_%H%M%S')
        output_directory = self.curve_config["outputDirectory"]

        if self.curve_config["saveFigToFile"]:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            img.save(f"{output_directory}/fig-{filename}.{file_format}",
                    format=file_format)

        if self.curve_config["saveDataToFile"]:
            with open(f"{output_directory}/fig-{filename}.txt", 'w') as datafile:
                for k, v in self.input_data.items():
                    datafile.write(f"{k}: {v}\n")

    def _set_hilbert_curve_properties(self) -> None:
        # set points and distance
        n = 2
        p = cpt.get_p_from_windspeed(self.input_data["WindSpeed"])
        hilbert_curve = HilbertCurve(p, n, n_procs=self.curve_config["processCount"])

        self.distances = np.arange(2 ** (p * n))
        self.points = np.asarray(hilbert_curve.points_from_distances(self.distances))
        self.p = p

        # set line colours
        start_line_colour = Color(
            cpt.line_temperature(round(self.input_data["MinTemperature"]))
        )
        end_line_colour = Color(
            cpt.line_temperature(round(self.input_data["MaxTemperature"]))
        )
        self.line_colour_range = np.fromiter(
            start_line_colour.range_to(end_line_colour, len(self.distances)),
            dtype="S16",
            count=len(self.distances),
        )

        # set background colormap
        self.bg_colormap = ListedColormap(cpt.bg_color_list(self.input_data['SignificantWeatherCode']))

    def _create_axes_instance(self) -> Axes:
        px = 1 / self.curve_config["displayDPI"]
        sizes = self.curve_config["imageDimensions"]
        fig = plt.figure(figsize=(sizes["width"] * px, sizes["height"] * px),
                        dpi=self.curve_config["displayDPI"])
        plt.subplots_adjust(left=0,
                            bottom=0,
                            right=1,
                            top=1,
                            wspace=0,
                            hspace=0)
        ax = fig.add_subplot()
        ax.set_aspect('auto', adjustable='box')
        plt.tick_params(left=False,
                        bottom=False,
                        labelleft=False,
                        labelbottom=False)
        for side in ['top', 'left', 'bottom', 'right']:
            ax.spines[side].set_visible(False)

        return ax
