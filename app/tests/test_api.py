import pytest
from api import api

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
