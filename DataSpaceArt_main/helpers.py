import os
import json
from dotenv import load_dotenv
from metoffice_weather_cli import weather


def load_config(path: str) -> tuple[dict]:
    with open(path) as config_file:
        config = json.load(config_file)
        curve_config = config["hilbertCurveProperties"]
        weather_config = config["weatherDataProperties"]

        load_dotenv()  # if .env is used, overwrite config.json with API key
        if os.environ["DATAHUB_API_KEY"]:
            weather_config["dataHubAPIKey"] = os.getenv("DATAHUB_API_KEY")

        return curve_config, weather_config


def get_weather_data(weather_config: dict) -> dict:
    return weather.get_weather_info(
        weather_config["city"] or "",
        weather_config["country"] or "",
        float(weather_config["coordinates"]["latt"]),
        float(weather_config["coordinates"]["longt"]),
    )
