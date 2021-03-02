# part of the data layer, reponsible for interacting with MongoDB

import os
from pymongo import MongoClient, DESCENDING


class WeatherCache():
    """Wrapps the weather collection from MongoDB and provide useful methods
    for the application to use it as a cache storage"""

    CACHE_EXPIRATION_TIME = 300  # in seconds

    @classmethod
    def _get_db(cls) -> None:
        mongo_uri = 'mongodb://{}:27017'.format(
            os.environ['MONGODB_HOSTNAME']
        )
        db_name = os.environ['MONGODB_DATABASE']
        return MongoClient(mongo_uri)[db_name]

    @classmethod
    def _get_weathers_collection(cls):
        if not hasattr(cls, '_weathers_collection'):
            db = cls._get_db()
            cls._weathers_collection = db.weathers
            # add index to optimize update_or_insert_weather and read_weather
            cls._weathers_collection.create_index('name')
            # add index to optimize read_latest_weathers and for TTL
            cls._weathers_collection.create_index(
                [('timestamp', DESCENDING)],
                expireAfterSeconds=cls.CACHE_EXPIRATION_TIME  # TTL policy
            )
        return cls._weathers_collection

    @staticmethod
    def _drop_surpluss_attrbs(dict_: dict) -> dict:
        """Remove unwanted attributes from dict returned by MongoDB"""
        SURPLUSS_ATTRBS = ['_id', 'timestamp']
        return {k: v for k, v in dict_.items() if k not in SURPLUSS_ATTRBS}

    @classmethod
    def update_or_insert_weather(cls, weather):
        """Update document with same name as the one in weather, otherwise
        insert new document"""
        cls._get_weathers_collection().update_one(
            {"name": weather['name']},
            {"$set": weather, "$currentDate": {"timestamp": True}},
            upsert=True
        )

    @classmethod
    def read_weather(cls, city_name):
        weather = cls._get_weathers_collection().find_one({'name': city_name})
        return cls._drop_surpluss_attrbs(weather) if weather else weather

    @classmethod
    def read_latest_weathers(cls, max: int = 5):
        return [cls._drop_surpluss_attrbs(weather) for weather in
                cls._get_weathers_collection().find().
                sort('timestamp', DESCENDING).limit(max)]
