from pymongo import MongoClient
from dotenv import load_dotenv
from api.utils.time import now
from api.models.user import User
from bson import ObjectId
from api.utils.db import db

import os

client = MongoClient(os.getenv("MONGO_URL"))
db = client["mydatabase"]

# add comment -> comment_id, push comment_id into book.comment[arr]
# get comment ->In Book call find_comment_of_book()->return content


class Comment:
    def __init__(
        self,
        commenter_id,
        review,
        rating,
        created_at=now(),
    ):
        self.commenter_id = commenter_id
        self.review = review
        self.rating = rating
        self.created_at = created_at

    def save(self):
        db.comments.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return db.comments.find()

    @staticmethod
    def find_comment_of_book(book_id):
        book_oid = ObjectId(book_id)
        book = db.books.find_one({"_id": book_oid})
        result = []
        for comments in book["comment_ids"]:
            oid = ObjectId(comments)
            result.append(db.comments.find_one({"_id": oid}))
        # pipeline = [
        #     {"$match": {"_id": book_oid}},
        #     {"$unwind": "$comment_ids"},
        #     {
        #         "$lookup": {
        #             "from": "comment_ids",
        #             "localField": "comment_ids",
        #             "foreignField": "_id",
        #             "as": "comments",
        #         }
        #     },
        #     {"$unwind": "$comments"},
        #     {
        #         "$project": {
        #             "comments" : "$comments"
        #         }
        #     },
        # ]
        # result = db.books.aggregate(pipeline)
        comment_list = []
        for comment in result:
            user = db.users.find_one(
                {"_id": ObjectId(comment["commenter_id"])})
            comment_list.append({
                "username": user['username'],
                "avatar": user['avatar'],
                "commenter_id": str(comment["commenter_id"]),
                "review": comment["review"],
                "rating": comment["rating"],
                "created_at": comment["created_at"]
            })
        return comment_list

    @staticmethod
    def update_created_at(comment_id, created_at):
        # ONLY USE IN INIT
        if not isinstance(comment_id, ObjectId):
            comment_id = ObjectId(comment_id)

        db.comments.update_one({"_id": comment_id}, {
                               "$set": {"created_at": created_at}})
