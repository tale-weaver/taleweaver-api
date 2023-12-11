from api.utils.time import now
from api.utils.db import db
import os



class Page:
    def __init__(
        self,
        image,
        description,
        book_id,
        interval_id,
        creator_id,
        voted_by_user_ids = [],
        created_at = now(),
        updated_at = now(),
        status='ongoing',
    ):
        # if not all([image, description, book_id, interval_id, creator_id, created_at]):
        #     raise ValueError("All fields are required")
        
        self.image = image
        self.description = description
        self.status = status
        self.book_id = book_id
        self.interval_id = interval_id
        self.creator_id = creator_id
        self.voted_by_user_ids = voted_by_user_ids
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        db.pages.insert_one(self.__dict__)

    @staticmethod
    def find_pages_by_bookid(book_id):
        pipeline = [
            {"$match": {"_id": book_id}},
            {"$unwind": "$page_ids"},
            {
                "$lookup": {
                    "from": "pages",
                    "localField": "page_ids",
                    "foreignField": "_id",
                    "as": "pages",
                }
            },
            {"$unwind": "$pages"},
            {
                "$project": {
                    "_id": 0,
                    "title": 1,
                    "pages.image": 1,
                    "pages.description": 1,
                    "pages.creator_id": 1,
                }
            },
        ]
        result = db.books.aggregate(pipeline)
        return result

    def find_page_by_pageid(page_id):
        page = db.pages.find_one({"_id": page_id}, {"_id": 0})
        return page

    def find_cover_by_bookid(book_id):
        book = db.books.find_one({"_id": book_id}, {"_id": 0, "page_ids": 1})
        if book and 'page_ids' in book:
            return book.page_ids[0]
        else:
            return None

    def save_as_fk(book_id, page_id):
        book = db.books.update_one({"_id": book_id}, {"$push": {"page_id": page_id}})
        return book

    def find_creator_by_id(page_id):
        creator_id = db.pages.find_one({"_id": page_id})["creator_id"]
        creator = db.users.find_one({"_id": creator_id})["username"]
        return creator
    
    def update_status_as_winner(page_id):
        page = db.pages.update_one({"_id": page_id}, {"$set": {"status": "winner"}})
        return page
    
    def update_status_as_loser(page_id):
        page = db.pages.update_one({"_id": page_id}, {"$set": {"status": "loser"}})
        return page
    
    def voted_by_user(page_id, user_id):
        page = db.pages.update_one({"_id": page_id}, {"$push": {"voted_by_user_ids": user_id}})
        return page