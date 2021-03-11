import os

import data
import werkzeug
from flask import Blueprint, jsonify, request

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/<city_name>', methods=['GET'])
def get_weather(city_name):
    try:
        weather = data.get_weather(city_name)
    except ValueError:
        raise werkzeug.exceptions.NotFound(
            '{} city not found.'.format(city_name)
        )
    return jsonify(weather)


@weather_bp.route('', methods=['GET'])
def get_weathers():
    DEFAULT_MAX = int(os.getenv('LATEST_WEATHERS_DEFAULT_MAX', 5))
    max = request.args.get('max', default=DEFAULT_MAX, type=int)
    weathers = data.get_latest_cached_weathers(max)
    return jsonify(weathers)
