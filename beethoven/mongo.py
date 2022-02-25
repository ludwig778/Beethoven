from pymongo import MongoClient

from beethoven.settings import mongo_config

mongo_instance = MongoClient(mongo_config.uri)
