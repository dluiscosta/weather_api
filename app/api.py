import os
from flask import Flask, jsonify, request
import werkzeug
import data
import logging


api = Flask(__name__)


@api.route('/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    try:
        weather = data.get_weather(city_name)
    except ValueError:
        raise werkzeug.exceptions.NotFound(
            '{} city not found.'.format(city_name)
        )
    return jsonify(weather)


@api.route('/weather', methods=['GET'])
def get_weathers():
    DEFAULT_MAX = int(os.getenv('LATEST_WEATHERS_DEFAULT_MAX', 5))
    max = request.args.get('max', default=DEFAULT_MAX, type=int)
    weathers = data.get_latest_cached_weathers(max)
    return jsonify(weathers)


@api.errorhandler(werkzeug.exceptions.HTTPException)
def handle_http_exception(e):
    status_code = e.get_response().status_code
    payload = {
        'message': e.description,
        'cod': status_code
    }
    return jsonify(payload), status_code


@api.errorhandler(Exception)
def handle_generic_exception(e):
    logging.error(e)
    payload = {
        'message': 'An internal error has occurred. '
                   'Please, contact the system administrator.',
        'cod': 500
    }
    return jsonify(payload), 500


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.getenv('PORT'))
