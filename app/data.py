# data layer responsible for dynamically fetching data from the cache DB or
# from the Open Weather API

from resources import open_weather
from typing import List


def get_weather(city_name: str) -> dict:
    # TODO: switch fetching between Open Weather API and cached DB
    return open_weather.get_weather_from_city_name(city_name)


def get_latest_cached_weathers(max: int = 5) -> List[dict]:
    raise NotImplementedError()
