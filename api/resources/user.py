from flask import request
from flask_restful import Resource
from api.models.user import User
from flask_bcrypt import Bcrypt
import random

bcrypt = Bcrypt()


class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']

        # Check if have all fields
        if not username or not password or not email:
            return {'message': 'Missing fields'}, 400

        # Check if username already exists
        if User.find_by_username(username, exclude=False):
            return {'message': 'Username already exists'}, 400

        # Create account
        verification_code = str(random.randint(100000, 999999))
        account = User(username, password, email,
                       verification_code=verification_code)
        account.save()

        return {'message': 'Account created successfully', 'verification_code': verification_code}, 201