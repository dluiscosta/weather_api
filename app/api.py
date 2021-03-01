import os
from flask import Flask, jsonify
from resources import open_weather
import data


api = Flask(__name__)


@api.route('/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    # TODO: handle invalid city name
    weather = data.get_weather(city_name)
    return jsonify(weather)


@api.errorhandler(open_weather.CityNotFound)
def handle_open_weather_city_not_found(e):
    payload = {
        'message': '{} city not found.'.format(e.searched_city_name),
        'cod': 404
    }
    return jsonify(payload), 404


@api.errorhandler(Exception)
def handle_open_weather_fetch_error(e):
    payload = {
        'message': 'An internal error has occurred. '
                   'Please, contact the system administrator.',
        'cod': 500
    }
    return jsonify(payload), 500


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.getenv('PORT'))
