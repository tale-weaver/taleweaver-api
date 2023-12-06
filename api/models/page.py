from pymongo import MongoClient
from dotenv import load_dotenv
import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["mydatabase"]


class Page:
    

    @staticmethod
    def find_by_bookname(bookname):
        book = db.books.find_one({"bookname": bookname}, {"_id": 0})
        return book
