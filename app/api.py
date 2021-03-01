import os
from flask import Flask
api = Flask(__name__)


@api.route('/weather/<city_name>', methods=['GET'])
def get_weather(city_name):
    raise NotImplementedError()


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=os.getenv('PORT'))
