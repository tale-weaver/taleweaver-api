from api.utils.time import now
from api.utils.db import db
from api.models.book import Book
from bson import ObjectId

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
        book_oid = ObjectId(book_id)
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

    def find_by_id(page_id, include_keys=[], exclude_keys=[]):
        page_oid = ObjectId(page_id)
        if include_keys and exclude_keys:
            projection = {k: 1 for k in include_keys}
            projection.update({k: 0 for k in exclude_keys})
            page = db.pages.find_one(
                {'_id': page_oid}, projection)
        elif include_keys:
            projection = {k: 1 for k in include_keys}
            page = db.pages.find_one(
                {'_id': page_oid}, projection)
        elif exclude_keys:
            projection = {k: 0 for k in exclude_keys}
            page = db.pages.find_one(
                {'_id': page_oid}, projection)
        else:
            page = db.pages.find_one({'_id': page_oid})
        return page

    def find_cover_by_bookid(book_id):
        book_oid = ObjectId(book_id)
        page_ids = db.books.find_one({"_id": book_oid}, {"_id": 0, "page_ids": 1})
        cover_id = page_ids['page_ids'][0]
        cover_oid = ObjectId(cover_id)
        cover = db.pages.find_one({"_id": cover_oid}, {"_id": 0})['image']
        print('cover:')
        print(cover)
        return cover

    def save_as_fk(book_id, page_id):
        book_oid = ObjectId(book_id)
        page_oid = ObjectId(page_id)
        book = db.books.update_one({"_id": book_oid}, {"$push": {"page_id": page_oid}})
        return book

    def find_creator_by_id(page_id):
        page_oid = ObjectId(page_id)
        page = db.pages.find_one({"_id": page_oid})
        print('page:')
        print(page)
        creator_id = page['creator_id']
        creator_oid = ObjectId(creator_id)
        creator = db.users.find_one({"_id": creator_oid})['username']
        print('creator:')
        print(creator)
        return creator
    
    def find_voting_pages(book_id):
        book_oid = ObjectId(book_id)
        book_current_interval_id = Book.find_by_id(book_id, include_keys=["interval_id"])
        book_current_interval_oid = ObjectId(book_current_interval_id)
        pipeline = [{
            '$match':{
            '$and':[
                {'book_id': book_oid},
                {'interval_id': book_current_interval_oid},
            ]
            }
        }]

        pages = db.pages.aggregate(pipeline)
        return pages

    def update_status_as_winner(page_id):
        page_oid = ObjectId(page_id)
        page = db.pages.update_one({"_id": page_oid}, {"$set": {"status": "winner"}})
        return page
    
    def update_status_as_loser(page_id):
        page_oid = ObjectId(page_id)
        page = db.pages.update_one({"_id": page_oid}, {"$set": {"status": "loser"}})
        return page
    
    def voted_by_user(page_id, user_id):
        page_oid = ObjectId(page_id)
        print('page_oid:')
        print(page_oid)
        user_oid = ObjectId(user_id)
        print('user_oid:')
        print(user_oid)
        page = db.pages.find_one({"_id": page_oid})
        if user_id in page['voted_by_user_ids']:
            db.pages.update_one({"_id": page_oid}, {"$pull": {"voted_by_user_ids": user_id}})
        else:
            db.pages.update_one({"_id": page_oid}, {"$push": {"voted_by_user_ids": user_id}})
        return page