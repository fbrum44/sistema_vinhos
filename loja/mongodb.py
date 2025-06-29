
from django.conf import settings
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)

db = client.get_database() 

vinhos_collection = db['vinhos']
usuarios_collection = db['usuarios']
historico_collection = db['historico']
