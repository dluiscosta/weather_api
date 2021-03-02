# Cacheable Open Weather Api Wrapper

This project consists in a code assessment challenge to wrap the public Open Weather API while caching it's returned data and exposing an endpoint to get a city's weather by it's name, as well as an endpoint to retrieve the latest cached city weathers.
The cached data lasts for 5 minutes.

**Caching is not yet implemented.**

## How to run

To run this project, you will need [Docker](https://www.docker.com/) installed. Then, from the directory of the cloned repository, simply run ```docker-compose up```. The API will be exposed locally at the port 5000.

To run in development mode, which automatically runs the tests, use ```docker-compose -f docker-compose.yml -f docker-compose.dev.yml up``` instead. The tests can be rerun by using ```docker start pytest```.

## Available endpoints

- ```/weather/<city_name>```: Get the weather data for the specified ```city_name```.  If available, cached data is used. Otherwise, new data is fetched from the Open Weather API and cached.
- ```/weather?max=<max_number>``` (**NOT YET IMPLEMENTED**): Get the weather data for all the cached cities, up to the latest ```max_number``` entries (if specified).