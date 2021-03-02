import pytest
import time
from api import api
from resources import open_weather
from resources.mongo_db import WeatherCache


VALID_CITY_NAME = 'New York'
INVALID_CITY_NAME = 'Old York'


@pytest.fixture
def client():
    api.config['TESTING'] = True
    with api.test_client() as client:
        WeatherCache._get_db().command("dropDatabase")
        if hasattr(WeatherCache, '_weathers_collection'):
            delattr(WeatherCache, '_weathers_collection')
        yield client


def test_valid_get_weather(client):
    response = client.get('weather/{}'.format(VALID_CITY_NAME))
    assert response.status_code == 200
    response_dict = response.get_json()
    assert response_dict['cod'] == 200
    assert response_dict['name'] == VALID_CITY_NAME


def test_invalid_get_weather(client):
    response = client.get('weather/{}'.format(INVALID_CITY_NAME))
    assert response.status_code == 404
    response_dict = response.get_json()
    assert response_dict['cod'] == 404
    assert 'message' in response_dict


def test_get_weather_cacheability(client):
    response1 = client.get('weather/{}'.format(VALID_CITY_NAME))
    response1_dict = response1.get_json()
    open_weather_endpoint = open_weather.ENDPOINT
    open_weather.ENDPOINT = 'invalid endpoint'  # block Open Weather API use
    try:
        response2 = client.get('weather/{}'.format(VALID_CITY_NAME))
        response2_dict = response2.get_json()
        assert response1_dict == response2_dict
    except Exception as e:
        raise e
    finally:
        open_weather.ENDPOINT = open_weather_endpoint


def test_get_weather_cache_expiration(client):
    weather_cache_expiration_time = WeatherCache.CACHE_EXPIRATION_TIME
    WeatherCache.CACHE_EXPIRATION_TIME = 5
    try:
        _ = client.get('weather/{}'.format(VALID_CITY_NAME))
        time.sleep(65)  # MongoDB checks for expired documents every 60 secs
        assert WeatherCache.read_weather(VALID_CITY_NAME) is None
    except Exception as e:
        raise e
    finally:
        WeatherCache.CACHE_EXPIRATION_TIME = weather_cache_expiration_time
