from pymongo import MongoClient
from dotenv import load_dotenv

import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["mydatabase"]


class Comment:
    def __init__(self, user_id, content, comment_date):
        self.user_id = user_id
        self.content = content
        self.comment_date = comment_date
    def save(self):
        db.comments.insert_one(self.__dict__)

    @staticmethod
    def find_comment_of_book(book_id):
        # do something
        return book_id
