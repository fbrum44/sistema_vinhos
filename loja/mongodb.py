
from django.conf import settings
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)

db = client.get_database() 

produtos_collection = db['produtos']
