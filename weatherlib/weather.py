import os
import json
import http.client
import urllib.parse
from dotenv import load_dotenv  # for dev purposes only


def get_weather(config):
    """Fetches the weather data for a given set of coordinates"""
    # connect to Weather DataHub
    load_dotenv()
    datahub_conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

    datahub_headers = {
        'X-IBM-Client-Id': os.getenv('DATAHUB_API_KEY'),
        'X-IBM-Client-Secret': os.getenv('DATAHUB_SECRET'),
        'accept': "application/json"
    }

    datahub_params = urllib.parse.urlencode({
        'excludeParameterMetadata': 'true',
        'includeLocationName': 'true',
        'latitude': config['coordinates']['latt'],
        'longitude': config['coordinates']['longt']
    })

    datahub_conn.request('GET',
                         '/metoffice/production/v0/forecasts/point/daily?{}'.format(datahub_params),
                         headers=datahub_headers
                         )

    datahub_res = datahub_conn.getresponse()
    datahub_data = datahub_res.read()
    if config["dumpDataToFile"]:
        with open('weather_dump.json', 'wb') as dumpfile:
            dumpfile.write(datahub_data)

    datahub_json = json.loads(datahub_data)
    time_series = datahub_json['features'][0]['properties']['timeSeries'][1]

    weather_data = {
        "SignificantWeatherCode": time_series['daySignificantWeatherCode'],
        "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
        "MinTemperature": time_series['dayLowerBoundMaxTemp'],
        "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'],  # %
        "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
        "MaxUvIndex": time_series['maxUvIndex']
    }
    return weather_data  # dict object


if __name__ == "__main__":
    with open("../config.json") as config_file:
        config = json.load(config_file)
        data = get_weather(config['weatherDataProperties'])
        print("Example request:\n", data)
