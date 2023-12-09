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
                 updated_at=now(),
                 book_ids=[],
                 comment_ids=[],
                 liked_book_ids=[],
                 saved_book_ids=[]
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
        self.updated_at = updated_at
        self.book_ids = book_ids
        self.comment_ids = comment_ids
        self.liked_book_ids = liked_book_ids
        self.saved_book_ids = saved_book_ids

    def save(self):
        db.users.insert_one(self.__dict__)

    @staticmethod
    def find_by_username(username):
        user = db.users.find_one({'username': username})
        return user
