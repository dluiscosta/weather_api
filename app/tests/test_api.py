import pytest
from api import api
from resources import open_weather

VALID_CITY_NAME = 'New York'
INVALID_CITY_NAME = 'Old York'


@pytest.fixture
def client():
    api.config['TESTING'] = True
    with api.test_client() as client:
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
