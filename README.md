# Cacheable Open Weather Api Wrapper

This project consists in a code assessment challenge to wrap the public [Open Weather API](https://openweathermap.org/api) while caching it's returned data and exposing an endpoint to get a city's current weather by it's name, as well as an endpoint to retrieve the latest cached city weathers.
The cached data lasts for a default of 5 minutes.

## How to run

To run this project, you will need [Docker](https://www.docker.com/) installed. Then, from the directory of the cloned repository, run one of the following commands:
- ```docker-compose up -d```, for the development stage;
- ```docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d```, for running the automated tests.
- ```docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d```, for the production stage.

For the development and production stage, the API will be exposed locally at the port 5000. In order to achieve testing that represents best the production stage, the API and the automated tests use the same container. Because of that, they currently can't be run simultaneously.
 
After running them once, the automated tests can be rerun by using ```docker start pytest```.

*DISCLAIMER*: The automated tests currently are taking long to run due to the ```test_get_weather_cache_expiration``` test. Even though this test reduces the configured cache expiration time, it still needs to wait at least 60 seconds in order to reliably assert if a given saved cache expired, since that is the duration of the cycle in which MongoDB checks for documents with expired [TTL](https://docs.mongodb.com/manual/core/index-ttl/).

## Available endpoints

- ```/weather/<city_name>```: Get the weather data for the specified ```city_name```.  If available, cached data is used. Otherwise, new data is fetched from the Open Weather API and cached.
- ```/weather?max=<max_number>```: Get the weather data for all the cached cities, up to the latest ```max_number``` entries (if specified).

## System Architecture

The system runs in two docker containers refering to the docker-compose services ```api-service```, which contains the application, and ```db-service```, which runs a [MongoDB](https://www.mongodb.com/) instance used for caching (automatically expiring with TTL).

At the application, the endpoints are defined at the ```api.py``` module using [Flask](https://flask.palletsprojects.com/en/1.1.x/), which in turn connects with the ```data.py``` module. The ```data.py``` module handles where to retrieve from and save data to by interacting with the resources modules ```open_weather.py``` and ```mongo_db.py```.

![Sytem Architecture Chart](https://i.ibb.co/T2tdV30/weather-diagram-1.png)

The automated tests, which use [pytest](https://docs.pytest.org/en/stable/), also run in the container referring to the docker-compose service ```api-service```, although not simultaneously with the full, exposed, API.
