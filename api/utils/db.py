from api.config.config import Config
from pymongo import MongoClient


client = MongoClient(Config.MONGO_URL)
db = client['mydatabase']
