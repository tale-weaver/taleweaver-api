from flask import request
from flask_restful import Resource
from api.models.user import User
from api.utils.templates import verification_email
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
import secrets

bcrypt = Bcrypt()
mail = Mail()


class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        source = data['source']

        # Check if have all fields
        if not username or not password or not email or not source:
            return {'message': 'Missing fields'}, 400

        # Check if username already exists
        if User.find_by_username(username):
            return {'message': 'Username already exists'}, 400

        account = User(username=username, password=password,
                       email=email, source=source)

        if source != 'credentials':
            account.is_verified = True
            return {'message': 'Account created successfully'}, 201

        verification_code = secrets.token_hex(32)
        account.verification_code = verification_code
        with mail.connect() as conn:
            html = verification_email(username, verification_code)
            subject = 'TaleWeaver Email Verification'
            msg = Message(subject, recipients=[email], html=html)
            conn.send(msg)

        return {'message': 'Account created successfully and verification email sent'}, 201


class UserResource(Resource):
    def get(self, username):
        user = User.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404
        return user, 200
