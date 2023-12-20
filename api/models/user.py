from api.utils.db import db
from flask_bcrypt import Bcrypt
from api.utils.time import now

bcrypt = Bcrypt()


class User:
    def __init__(self,
                 username,
                 password,
                 email,
                 source,
                 role='user',
                 avatar='',
                 is_verified=False,
                 verification_code='',
                 created_at=now(),
                 ):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')
        self.email = email
        self.source = source
        self.role = role
        self.avatar = avatar
        self.is_verified = is_verified
        self.verification_code = verification_code
        self.created_at = created_at

    def save(self):
        db.users.insert_one(self.__dict__)

    @staticmethod
    def find_by_username(username, include_keys=[], exclude_keys=[]):

        if include_keys and exclude_keys:
            projection = {k: 1 for k in include_keys}
            projection.update({k: 0 for k in exclude_keys})
            user = db.users.find_one(
                {'username': username}, projection)
        elif include_keys:
            projection = {k: 1 for k in include_keys}
            user = db.users.find_one(
                {'username': username}, projection)
        elif exclude_keys:
            projection = {k: 0 for k in exclude_keys}
            user = db.users.find_one(
                {'username': username}, projection)
        else:
            user = db.users.find_one({'username': username})

        return user

    @staticmethod
    def update(user, update_dict):
        user.update(update_dict)
        db.users.update_one({'username': user['username']}, {
                            '$set': user})

    @staticmethod
    def get_all():
        users = db.users.find()
        return users

    @staticmethod
    def get_profile_data(username):

        # get user
        user = db.users.find_one({'username': username})

        # using user _id to get all pages they created
        pages = db.pages.find({'creator_id': user['_id']})

        # using user _id to get all books they liked
        books = db.books.find({"liked_by_user_ids": {"$in": [user['_id']]}})

        # using user _id to get all comments they made
        comments = db.comments.find({'commenter_id': user['_id']})

        profile_data = {
            'user': user,
            'pages': list(pages),
            'books': list(books),
            'comments': list(comments)
        }

        return profile_data
