# tuples of hex colors for passing into Color objects to create colormaps

clear = ('#5c92cb', '#b3f8fb')
cloudy = ('#9a9e8f', '#f2f2f2')
mist = ('#b0b9d9', '#e5f2fd')
light_rain = ('#4b529e', '#b8c4ef')
heavy_rain = ('#2427cc', '#00b2ff')
sleet_hail = ('#eaeaea', '#5aa4c4')
snow = ('#66dbff', '#f4f4f4')
thunder = ('#e138ff', '#fff95b')

code_to_colours = {
    'NA': clear,
    '0': clear,
    '1': clear,
    '2': clear,
    '3': clear,
    '4': clear,  # not used
    '5': mist,
    '6': mist,
    '7': cloudy,
    '8': cloudy,
    '9': light_rain,
    '10': light_rain,
    '11': light_rain,
    '12': light_rain,
    '13': heavy_rain,
    '14': heavy_rain,
    '15': heavy_rain,
    '16': sleet_hail,
    '17': sleet_hail,
    '18': sleet_hail,
    '19': sleet_hail,
    '20': sleet_hail,
    '21': sleet_hail,
    '22': snow,
    '23': snow,
    '24': snow,
    '25': snow,
    '26': snow,
    '27': snow,
    '28': thunder,
    '29': thunder,
    '30': thunder
}

code_to_weather_type = {
    'NA': 'Not available',
    '0': 'Clear night',
    '1': 'Sunny day',
    '2': 'Partly cloudy (night)',
    '3': 'Partly cloudy (day)',
    '4': 'Not used',
    '5': 'Mist',
    '6': 'Fog',
    '7': 'Cloudy',
    '8': 'Overcast',
    '9': 'Light rain shower (night)',
    '10': 'Light rain shower (day)',
    '11': 'Drizzle',
    '12': 'Light rain',
    '13': 'Heavy rain shower (night)',
    '14': 'Heavy rain shower (day)',
    '15': 'Heavy rain',
    '16': 'Sleet shower (night)',
    '17': 'Sleet shower (day)',
    '18': 'Sleet',
    '19': 'Hail shower (night)',
    '20': 'Hail shower (day)',
    '21': 'Hail',
    '22': 'Light snow shower (night)',
    '23': 'Light snow shower (day)',
    '24': 'Light snow',
    '25': 'Heavy snow shower (night)',
    '26': 'Heavy snow shower (day)',
    '27': 'Heavy snow',
    '28': 'Thunder shower (night)',
    '29': 'Thunder shower (day)',
    '30': 'Thunder'
}