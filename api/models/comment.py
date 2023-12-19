from pymongo import MongoClient
from dotenv import load_dotenv
from api.utils.time import now
from bson import ObjectId

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
        updated_at=now(),
    ):
        self.commenter_id = commenter_id
        self.review = review
        self.rating = rating
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        db.comments.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return db.comments.find()

    @staticmethod
    def find_comment_of_book(book_id):
        book_oid = ObjectId(book_id)
        pipeline = [
            {"$match": {"_id": book_oid}},
            {"$unwind": "$comment_ids"},
            {
                "$lookup": {
                    "from": "books",
                    "localField": "comment_ids",
                    "foreignField": "_id",
                    "as": "comments",
                }
            },
            {"$unwind": "$comments"},
            {
                "$project": {
                    "comments" : "$comments"
                }
            },
        ]
        result = db.books.aggregate(pipeline)
        comment_list = []
        for comment in result:
            print(comment)
            user = db.users.find_one({"_id": ObjectId(comment["comments"]["commenter_id"])})
            comment_list.append({
                "username": user['username'],
                "avatar": user['avatar'],
                "commenter_id": str(comment["comments"]["commenter_id"]),
                "image": comment["comments"]["image"],
                "created_at": comment["comments"]["created_at"]
            })        
        return comment_list
