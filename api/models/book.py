from api.utils.db import db
from api.utils.time import now
from api.models.user import User
from bson import ObjectId
from bson.json_util import loads, dumps


class Book:
    def __init__(
        self,
        title,
        current_interval_id,
        status="submitting",
        page_ids = [],
        comment_ids = [],
        liked_by_user_ids = [],
        interval_ids = [],
        created_at = now(),
        updated_at = now(),
    ):
        self.title = title
        self.page_ids = page_ids
        self.validate(status)
        self.current_interval_id = current_interval_id
        self.status = status
        self.comment_ids = comment_ids
        self.liked_by_user_ids = liked_by_user_ids
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
    def find_by_id(book_id, include_keys=[], exclude_keys=[]):
        book_oid = ObjectId(book_id)
        if include_keys and exclude_keys:
            projection = {k: 1 for k in include_keys}
            projection.update({k: 0 for k in exclude_keys})
            book = db.books.find_one(
                {'_id': book_oid}, projection)
        elif include_keys:
            projection = {k: 1 for k in include_keys}
            book = db.books.find_one(
                {'_id': book_oid}, projection)
        elif exclude_keys:
            projection = {k: 0 for k in exclude_keys}
            book = db.books.find_one(
                {'_id': book_oid}, projection)
        else:
            book = db.books.find_one({'_id': book_oid})
        return book

    def find_all_books():
        book = db.books.find()
        return book
    
    def find_all_books_by_status(status):
        book = db.books.find({"status": status})
        return book
    
    def push_new_page(book_id, page_id):
        book_oid = ObjectId(book_id)
        page_oid = ObjectId(page_id)
        db.books.update_one({"_id": book_oid}, {"$push": {"page_ids": page_oid}})
        book = db.books.find_one({"_id": book_oid})
        return book
    
    def liked_by_user(book_id, user_id):
        book_oid = ObjectId(book_id)
        user_oid = ObjectId(user_id)
        book = db.books.find_one({"_id": book_oid})
        if user_id in book['liked_by_user_ids']:
            db.books.update_one({"_id": book_oid}, {"$pull": {"liked_by_user_ids": user_id}})
            
            # User.update()
            
        else:
            db.books.update_one({"_id": book_oid}, {"$push": {"liked_by_user_ids": user_id}})
        book = db.books.find_one({"_id": book_oid})
        # 還沒做 User 的 liked_book_ids 更新
        return book
    
    def update_status_by_bookid(book_id, status):
        book_oid = ObjectId(book_id)
        db.books.update_one({"_id": book_oid}, {"$set": {"status": status}})
        book = db.books.find_one({"_id": book_oid})
        return book

    def push_comment(book_id, comment_id):
        book_oid = ObjectId(book_id)
        comment_oid = ObjectId(comment_id)
        db.books.update_one({"_id": book_oid}, {"$push": {"comment_ids": comment_oid}})
        book = db.books.find_one({"_id": book_oid})
        return book
    
    