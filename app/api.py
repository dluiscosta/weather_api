import os
from flask import Flask, jsonify
import data


api = Flask(__name__)


@api.route('/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    # TODO: handle invalid city name
    weather = data.get_weather(city_name)
    return jsonify(weather)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.getenv('PORT'))
