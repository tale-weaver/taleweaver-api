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
            content, 
            created_at=now(),
            updated_at=now(),
        ):
        self.commenter_id = commenter_id
        self.content = content
        self.created_at =  created_at
        self.updated_at = updated_at
        
    def save(self):
        db.comments.insert_one(self.__dict__)

    @staticmethod
    def find_comment_of_book(book_id):
        book_oid = ObjectId(book_id)
        pipeline = [
            {"$match": {"_id": book_oid}},
            {"$unwind": "$comment_ids"},
            {
                "$lookup": {
                    "from": "pages",
                    "localField": "comment_ids",
                    "foreignField": "_id",
                    "as": "comments",
                }
            },
            {"$unwind": "$comments"},
            {
                "$project": {
                    "_id": 0,
                    "comments.commenter_id": 1,
                    "comments.image": 1,
                    "comments.created_at": 1,
                }
            },
        ]
        result = db.books.aggregate(pipeline)
        return result
