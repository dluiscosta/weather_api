# part of the data layer, responsible for connecting with the Open Weather API

import requests
import os

ENDPOINT = os.environ['OPEN_WEATHER_ENDPOINT']
API_KEY = os.environ['OPEN_WEATHER_API_KEY']


class CityNotFound(ValueError):

    def __init__(self, searched_city_name):
        self.searched_city_name = searched_city_name


class FetchError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def get_weather_from_city_name(city_name: str) -> dict:
    """Fetch a city's weather, through it's name, from the Open Weather API"""
    query_params = {'q': city_name, 'appid': API_KEY}
    response = requests.get(ENDPOINT, params=query_params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise CityNotFound(city_name)
    else:
        raise FetchError(response.status_code, response.json()['message'])
