from plotter import HilberCurvePlotter
from helpers import load_config, get_weather_data


def main():
    curve_config, weather_config = load_config('config.json')

    input_data = get_weather_data(weather_config)
    if weather_config['printDataToConsole']:
        print("Input data log:")
        for k, v in input_data.items():
            print(f"{k}: {v}")

    plotter = HilberCurvePlotter(input_data, curve_config)
    plotter.plot()
    plotter.save()


if __name__ == '__main__':
    main()
