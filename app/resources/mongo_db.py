import os
from pymongo import MongoClient, DESCENDING


class WeatherCache():

    @classmethod
    def init_db(cls, db_uri: str = None) -> None:
        db_uri = 'mongodb://{}:27017/{}'.format(
            os.environ['MONGODB_HOSTNAME'],
            os.environ['MONGODB_DATABASE']
        ) if not db_uri else db_uri
        cls._weathers_collection = MongoClient(db_uri).cache.weathers
        cls._weathers_collection.create_index('name')
        cls._weathers_collection.create_index([('timestamp', DESCENDING)])

    @staticmethod
    def _drop_surpluss_attrbs(dict_: dict) -> dict:
        SURPLUSS_ATTRBS = ['_id', 'timestamp']
        return {k: v for k, v in dict_.items() if k not in SURPLUSS_ATTRBS}

    @classmethod
    def update_or_insert_weather(cls, weather):
        cls._weathers_collection.update_one(
            {"name": weather['name']},
            {"$set": weather, "$currentDate": {"timestamp": True}},
            upsert=True
        )

    @classmethod
    def read_weather(cls, city_name):
        weather = cls._weathers_collection.find_one({'name': city_name})
        return cls._drop_surpluss_attrbs(weather) if weather else weather

    @classmethod
    def read_latest_weathers(cls, max: int = 5):
        return [cls._drop_surpluss_attrbs(weather) for weather in
                cls._weathers_collection.find().sort('timestamp', DESCENDING).
                limit(max)]


WeatherCache.init_db()
