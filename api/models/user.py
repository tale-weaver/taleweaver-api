from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os

client = MongoClient(os.getenv('MONGO_URL'))
db = client['mydatabase']
bcrypt = Bcrypt()


class User:
    def __init__(self, username, password, email, avatar='', verification_code='', is_verified=False):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')
        self.email = email
        self.avatar = avatar
        self.verification_code = verification_code
        self.is_verified = is_verified

    def save(self):
        db.users.insert_one(self.__dict__)

    @staticmethod
    def find_by_username(username, exclude=True):
        user = db.users.find_one({'username': username}, {'_id': 0})
        return user