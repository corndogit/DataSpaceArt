import json
import http.client
import urllib.parse


def get_weather(config):
    """Fetches the weather data for a given set of coordinates"""
    # connect to Weather DataHub
    datahub_conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

    datahub_headers = {
        'X-IBM-Client-Id': config["dataHubAPIKey"],
        'X-IBM-Client-Secret': config["dataHubSecret"],
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
        with open('../bin/weather_dump.json', 'wb') as dumpfile:
            dumpfile.write(datahub_data)
            print("request dumped to /bin/weather_dump.json")

    datahub_json = json.loads(datahub_data)
    try:
        time_series = datahub_json['features'][0]['properties']['timeSeries'][1]
    except KeyError:
        return ": ".join(datahub_json.values())

    weather_data = {
        "SignificantWeatherCode": time_series['daySignificantWeatherCode'],
        "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
        "MinTemperature": time_series['dayLowerBoundMaxTemp'],
        "MeanSeaLevelPressure": time_series['middayMslp'],  # bar
        "Visibility": time_series['middayVisibility'],  # m
        "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'] / 100,  # %
        "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
        "WindDirection": time_series['midday10MWindDirection'],  # bearing
        "RelativeHumidity": time_series['middayRelativeHumidity'] / 100,  # %
        "MaxUvIndex": time_series['maxUvIndex'],
        "ProbabilityOfSnow": time_series['dayProbabilityOfSnow'] / 100,  # %
        "ProbabilityOfHail": time_series['dayProbabilityOfHail'] / 100,  # %
        "ProbabilityOfSferics": time_series['dayProbabilityOfSferics'] / 100  # %
    }
    return weather_data


if __name__ == "__main__":
    with open("../config.json") as config_file:
        cfg = json.load(config_file)
        data = get_weather(cfg['weatherDataProperties'])
        print("Example request:")
        for k, v in data.items():
            print(f"{k}: {v}")
