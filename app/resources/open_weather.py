# data layer responsible for connecting with the Open Weather API and fetching
# valid data

import requests

ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = '09d9c578d13c2303e83f7b7f94f12d3f'


def get_weather_from_city_name(city_name: str) -> dict:
    # TODO: handle failure on fetching data
    # TODO: specify weather schema to validate data and remove surpluss attrbs
    query_params = {'q': city_name, 'appid': API_KEY}
    response = requests.get(ENDPOINT, params=query_params)
    return response.json()
