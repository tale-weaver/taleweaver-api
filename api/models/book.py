from api.utils.db import db
from api.utils.time import now, create_time_intervals
from api.models.user import User
from bson import ObjectId


class Book:
    def __init__(
        self,
        title,
        cover,
        description,
        cover="",
        page_ids=[],
        comment_ids=[],
        liked_by_user_ids=[],
        interval_ids=create_time_intervals(now()),
        created_at=now(),
        updated_at=now(),
    ):
        self.title = title
        self.cover = cover
        self.description = description
        self.cover = cover
        self.page_ids = page_ids
        self.comment_ids = comment_ids
        self.liked_by_user_ids = liked_by_user_ids
        self.interval_ids = interval_ids
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = interval_ids[0]["status"]
        self.round = interval_ids[0]["round"]

        self.validate(self.status)

    def save(self):
        db.books.insert_one(self.__dict__)

    def validate(self, status):
        valid_status = ["finished", "submitting", "voting"]

        if status not in valid_status:
            raise ValueError("Status must be one of {}".format(valid_status))

    @staticmethod
    def get_all():
        return db.books.find()

    @staticmethod
    def update_cover(book_id, cover_url):

        if not isinstance(book_id, ObjectId):
            book_id = ObjectId(book_id)

        db.books.update_one({"_id": book_id}, {"$set": {"cover": cover_url}})

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

    @staticmethod
    def update(book, update_dict):
        book.update(update_dict)
        db.books.update_one({'title': book['title']}, {
                            '$set': book})
    @staticmethod
    def find_all_books():
        book = db.books.find()
        return book

    @staticmethod
    def find_books_by_status(status):
        book = db.books.find({"status": status})
        return book
    
    @staticmethod
    def find_winner_pages(book_id):
        book_oid = ObjectId(book_id)
        book = Book.find_by_id(book_id)
        pipeline = [
            {"$match": {"_id": book_oid}},
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
                    "pages": "$pages",
                }
            },
        ]
        result = db.books.aggregate(pipeline)
        # _id of result is book_id an ['pages'] is a list of pages
        print('result:')
        formatted_book = []
        for item in result:
            formatted_book.append(item['pages'])
        print(formatted_book)
        return formatted_book

    @staticmethod
    def push_new_page(book_id, page_id):
        book_oid = ObjectId(book_id)
        page_oid = ObjectId(page_id)
        db.books.update_one({"_id": book_oid}, {
                            "$push": {"page_ids": page_oid}})
        book = db.books.find_one({"_id": book_oid})
        return book

    @staticmethod
    def liked_by_user(book_id, username):
        book_oid = ObjectId(book_id)
        book = db.books.find_one({"_id": book_oid})
        user = User.find_by_username(username)
        user_id = user["_id"]
        user_oid = ObjectId(user_id)
        if user_oid in book['liked_by_user_ids']:
            db.books.update_one({"_id": book_oid}, {
                                "$pull": {"liked_by_user_ids": user_oid}})
        else:
            db.books.update_one({"_id": book_oid}, {
                                "$push": {"liked_by_user_ids": user_oid}})
        book = db.books.find_one({"_id": book_oid})
        return book

    @staticmethod
    def push_comment(book_id, comment_id, user_id):
        book_oid = ObjectId(book_id)
        comment_oid = ObjectId(comment_id)
        user_oid = ObjectId(user_id)
        db.books.update_one({"_id": book_oid}, {
                            "$push": {"comment_ids": comment_oid}})
        db.users.update_one({"_id": user_oid}, {
                            "$push": {"comment_ids": comment_oid}})
        book = db.books.find_one({"_id": book_oid})
        return book
