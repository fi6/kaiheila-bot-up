import os
from pymongo import MongoClient
from pymongo.collection import Collection

client = MongoClient(os.environ.get('MONGO_URL'))
db = client['test_db']

archives: Collection = db['archives']
subscribes: Collection = db['subscribes']
