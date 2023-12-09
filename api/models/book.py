from pymongo import MongoClient
from dotenv import load_dotenv

import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["mydatabase"]


class Book:
    def __init__(
        self,
        title,
        page_ids,
        status,
        comment_ids,
        liked_by_user_ids,
        saved_by_user_ids,
        interval_ids,
        created_at,
        updated_at,
    ):
        self.title = title
        self.page_ids = page_ids
        self.validate(status)
        self.status = status
        self.comment_ids = comment_ids
        self.liked_by_user_ids = liked_by_user_ids
        self.saved_by_user_ids = saved_by_user_ids
        self.interval_ids = interval_ids
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        db.books.insert_one(self.__dict__)
    def validate(self, status):
        valid_status = ["finished", "submitting", "voting"]
        if status not in valid_status:
            raise ValueError("Status must be one of {}".format(valid_status))
    
    @staticmethod
    def find_by_bookid(book_id):
        book = db.books.find_one({"_id": book_id}, {"_id": 0})
        return book

    def find_all_books():
        book = db.books.find({})
        return book
    
    def find_all_books_by_status(status):
        book = db.books.find({"status": status})
        return book
    
    def push_new_page(book_id, page_id):
        book = db.books.update_one({"_id": book_id}, {"$push": {"page_ids": page_id}})
        return book
    
    def liked_by_user(book_id, user_id):
        book = db.books.update_one({"_id": book_id}, {"$push": {"liked_by_user_ids": user_id}})
        return book
    
    def saved_by_user(book_id, user_id):
        book = db.books.update_one({"_id": book_id}, {"$push": {"saved_by_user_ids": user_id}})
        return book
    
    def update_status_by_bookid(book_id, status):
        book = db.books.update_one({"_id": book_id}, {"$set": {"status": status}})
        return book
    
    def remove_like_by_user(book_id, user_id):
        book = db.books.update_one({"_id": book_id}, {"$pull": {"liked_by_user_ids": user_id}})
        return book
    
    def remove_save_by_user(book_id, user_id):
        book = db.books.update_one({"_id": book_id}, {"$pull": {"saved_by_user_ids": user_id}})
        return book

    
    
    