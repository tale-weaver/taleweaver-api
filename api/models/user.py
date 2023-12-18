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
