# Cacheable Open Weather Api Wrapper

This project consists in a code assessment challenge to wrap the public [Open Weather API](https://openweathermap.org/api) while caching it's returned data and exposing an endpoint to get a city's current weather by it's name, as well as an endpoint to retrieve the latest cached city weathers.
The cached data lasts for a default of 5 minutes.

## How to run

To run this project, you will need [Docker](https://www.docker.com/) installed. Then, from the directory of the cloned repository, simply run ```docker-compose up```. The API will be exposed locally at the port 5000.

To run in development mode, which automatically runs the tests, use ```docker-compose -f docker-compose.yml -f docker-compose.dev.yml up``` instead. The tests can be rerun by using ```docker start pytest```.

## Available endpoints

- ```/weather/<city_name>```: Get the weather data for the specified ```city_name```.  If available, cached data is used. Otherwise, new data is fetched from the Open Weather API and cached.
- ```/weather?max=<max_number>```: Get the weather data for all the cached cities, up to the latest ```max_number``` entries (if specified).

## System Architecture

The system runs in two docker containers refering to the docker-compose services ```api-service```, which contains the application, and ```db-service```, which runs a [MongoDB](https://www.mongodb.com/) instance used for caching (automatically expiring with TTL).

At the application, the endpoints are defined at the ```api.py``` module using [Flask](https://flask.palletsprojects.com/en/1.1.x/), which in turn connects with the ```data.py``` module. The ```data.py``` module handles where to retrieve from and save data to by interacting with the resources modules ```open_weather.py``` and ```mongo_db.py```.

![Sytem Architecture Chart](https://i.ibb.co/T2tdV30/weather-diagram-1.png)

The automated tests run in a third, independent container, refering to the docker-compose service ```api-tests-service```. It uses the same image and configurations as ```api-service``` and, with [pytest](https://docs.pytest.org/en/stable/), is only run at the development stage.
