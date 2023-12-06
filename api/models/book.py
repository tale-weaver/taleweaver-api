from pymongo import MongoClient
from dotenv import load_dotenv

import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["mydatabase"]

class Book:
    def __init__(self, bookname, page_id, status, comment, like):
        self.bookname = bookname
        self.page_id = page_id
        self.status = status
        self.comment = comment
        self.like = like

    def save(self):
        db.books.insert_one(self.__dict__)

    @staticmethod
    def find_by_bookname(bookname):
        book = db.books.find_one({"bookname": bookname}, {"_id": 0})
        return book
    def find_all_books():
        book = db.books.find({})
