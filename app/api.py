import logging
import os

import werkzeug
from flask import Flask, jsonify
from weather import weather_bp

api = Flask(__name__)
api.register_blueprint(weather_bp, url_prefix='/weather')


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
