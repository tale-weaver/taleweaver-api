from api.utils.time import now
from api.utils.db import db
from api.models.book import Book
from bson import ObjectId


class Page:
    def __init__(
        self,
        image,
        title,
        description,
        creator_id,
        status="ongoing",
        voted_by_user_ids=[],
        created_at=now(),
    ):
        self.image = image
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.status = status
        self.voted_by_user_ids = voted_by_user_ids
        self.created_at = created_at

    def save(self):
        db.pages.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return db.pages.find()
    
    @staticmethod
    def update(page, update_dict):
        page.update(update_dict)
        db.pages.update_one({'title': page['title']}, {
                            '$set': page})

    @staticmethod
    def find_pages_by_bookid(book_id):
        book_oid = ObjectId(book_id)
        book = Book.find_by_id(book_id)
        status = book['status']
        match_condition = {}
        if status == 'finished':
            return {}
        if status == 'submitting' or 'voting':
            match_condition = {"$match": {"pages.status": "ongoing"}}

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
            match_condition,
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

    @staticmethod
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

    @staticmethod
    def update_status(page_id, status):

        if isinstance(page_id, ObjectId):
            page_id = ObjectId(page_id)

        assert status in [
            "winner", "loser"], "Status must be either 'winner' or 'loser'"

        page = db.pages.update_one(
            {"_id": page_id}, {"$set": {"status": status}}
        )

        return page

    @staticmethod
    def update_created_at(page_id, time):
        # THIS METHOD IS ONLY USED IN INIT

        if not isinstance(page_id, ObjectId):
            page_id = ObjectId(page_id)

        page = db.pages.update_one(
            {"_id": page_id}, {"$set": {"created_at": time}}
        )

        return page

    @staticmethod
    def voted_by_user(page_id, user_id, unvote=False) -> bool:

        if not isinstance(page_id, ObjectId):
            page_id = ObjectId(page_id)

        if not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)

        page = db.pages.find_one({"_id": page_id})

        if not unvote:
            if user_id in page['voted_by_user_ids']:
                return False
            db.pages.update_one({"_id": page_id}, {
                                "$push": {"voted_by_user_ids": user_id}})
            return True

        if user_id not in page['voted_by_user_ids']:
            return False

        db.pages.update_one({"_id": page_id}, {
                            "$pull": {"voted_by_user_ids": user_id}})
        return True
