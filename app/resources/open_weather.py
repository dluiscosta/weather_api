# data layer responsible for connecting with the Open Weather API and fetching
# valid data

import requests
import logging

ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = '09d9c578d13c2303e83f7b7f94f12d3f'


class CityNotFound(ValueError):

    def __init__(self, searched_city_name):
        self.searched_city_name = searched_city_name


class FetchError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def get_weather_from_city_name(city_name: str) -> dict:
    query_params = {'q': city_name, 'appid': API_KEY}
    response = requests.get(ENDPOINT, params=query_params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise CityNotFound(city_name)
    else:
        raise FetchError(response.status_code, response.json()['message'])
