import pytest
import time
from api import api
from resources import open_weather
from resources.mongo_db import WeatherCache


VALID_CITY_NAME = 'New York'
INVALID_CITY_NAME = 'Old York'
VALID_CITIES_NAMES_LIST = [
    'Paris', 'New York', 'London', 'Bangkok', 'Hong Kong', 'Dubai']


@pytest.fixture
def client():
    api.config['TESTING'] = True
    with api.test_client() as client:
        # clear database and WeatherCache before each test
        WeatherCache._get_db().command("dropDatabase")
        if hasattr(WeatherCache, '_weathers_collection'):
            delattr(WeatherCache, '_weathers_collection')
        yield client


def test_valid_get_weather(client):
    """Asserts if the endpoint /weather/<city_name> is running and returns a
    valid JSON containing the pair name=city_name"""
    response = client.get('weather/{}'.format(VALID_CITY_NAME))
    assert response.status_code == 200
    response_dict = response.get_json()
    assert response_dict['cod'] == 200
    assert response_dict['name'] == VALID_CITY_NAME


def test_invalid_get_weather(client):
    """Asserts if a call to /weather/<city_name> with an invalid city_name
    properly results in a recognizable 404 response, allowing the user to
    correct the parameter"""
    response = client.get('weather/{}'.format(INVALID_CITY_NAME))
    assert response.status_code == 404
    response_dict = response.get_json()
    assert response_dict['cod'] == 404
    assert 'message' in response_dict


def test_get_weather_cacheability(client):
    """Asserts if a previously fetched city weather is cached by requesting
    it again after blocking the application's access to the Open Weather API"""
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
    """Asserts if the cached city weathers are properly expiring after the
    configured time"""
    weather_cache_expiration_time = WeatherCache.CACHE_EXPIRATION_TIME
    WeatherCache.CACHE_EXPIRATION_TIME = 5  # reduced to reduce test time
    try:
        _ = client.get('weather/{}'.format(VALID_CITY_NAME))
        wait_for = 60 + WeatherCache.CACHE_EXPIRATION_TIME  # in seconds
        time.sleep(wait_for)  # MongoDB checks expired documents every 60 sec.
        assert WeatherCache.read_weather(VALID_CITY_NAME) is None
    except Exception as e:
        raise e
    finally:
        WeatherCache.CACHE_EXPIRATION_TIME = weather_cache_expiration_time


def test_get_latest_cached_weathers(client):
    """Asserts if the endpoint /weather?max=<max_number> is running and
    correctly selecting the latest cached city weathers, up to both a specified
    entries limit or the default"""
    for city_name in VALID_CITIES_NAMES_LIST:
        _ = client.get('weather/{}'.format(city_name))
    response = client.get('weather?max=3')
    response_list = response.get_json()
    response_city_names = [weather['name'] for weather in response_list]
    assert(set(response_city_names) == set(VALID_CITIES_NAMES_LIST[-3:]))
    response = client.get('weather')
    response_list = response.get_json()
    response_city_names = [weather['name'] for weather in response_list]
    assert(set(response_city_names) == set(VALID_CITIES_NAMES_LIST[-5:]))


def test_invalid_endpoint(client):
    """Asserts if a call to an invalid endpoint properly results in a
    recognizable 404 response, allowing the user to correct the API call"""
    response = client.get('invalid_enpoint')
    assert response.status_code == 404
    response_dict = response.get_json()
    assert response_dict['cod'] == 404
    assert 'message' in response_dict
