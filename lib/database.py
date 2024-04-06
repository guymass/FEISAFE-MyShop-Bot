from mongoengine import *
from urllib import parse
from pymongo import MongoClient
from settings import (mongo_host, mongo_user, mongo_password, mongo_collection)

username = parse.quote_plus(mongo_user)
password = parse.quote_plus(mongo_password)
client = MongoClient('mongodb://%s:%s@%s:17474/' % (username, password, mongo_host), unicode_decode_error_handler='ignore')

db = client[mongo_collection]