# data layer responsible for dynamically fetching data from the cache DB or
# from the Open Weather API

from resources import open_weather
from resources.mongo_db import WeatherCache
from typing import List


def get_weather(city_name: str) -> dict:
    weather = WeatherCache.read_weather(city_name)
    if not weather:
        weather = open_weather.get_weather_from_city_name(city_name)
        WeatherCache.update_or_insert_weather(weather)
    return weather


def get_latest_cached_weathers(max: int = 5) -> List[dict]:
    raise NotImplementedError()
