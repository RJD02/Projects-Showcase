from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/DevSearch')
db = client['DevSearch']
