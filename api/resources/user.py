from flask import request
from flask_restful import Resource
from api.models.user import User
from api.utils.templates import verification_email
from api.utils.time import now
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        avatar = data['avatar'] or "https://gravatar.com/avatar/b6eada68a0879b7af38a4ddf32e06aa7?s=400&d=robohash&r=x"

        # Check if have all fields
        if not username or not password or not email or not source:
            return {'message': 'Missing fields'}, 400

        # Check if username already exists
        if User.find_by_username(username):
            return {'message': 'Username already exists'}, 400

        account = User(username=username, password=password,
                       email=email, source=source, avatar=avatar)

        if source != 'credentials':
            account.is_verified = True
            account.save()
            return {'message': 'Account created successfully'}, 201

        verification_code = secrets.token_hex(32)
        account.verification_code = verification_code
        account.save()
        with mail.connect() as conn:
            html = verification_email(username, verification_code)
            subject = 'TaleWeaver Email Verification'
            msg = Message(subject, recipients=[email], html=html)
            conn.send(msg)

        return {'message': 'Account created successfully and verification email sent'}, 201


class ResendVerificationEmail(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']

        # Check if have all fields
        if not username:
            return {'message': 'Missing fields'}, 400

        user = User.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404

        if user['is_verified']:
            return {'message': 'User already verified'}, 400

        verification_code = secrets.token_hex(32)
        User.update(user, {
            'verification_code': verification_code,
            'updated_at': now()
        })
        with mail.connect() as conn:
            html = verification_email(username, verification_code)
            subject = 'TaleWeaver Email Verification'
            msg = Message(subject, recipients=[user['email']], html=html)
            conn.send(msg)

        return {'message': 'Verification email sent'}, 200


class VerifyEmail(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        verification_code = data['token']

        # Check if have all fields
        if not username or not verification_code:
            return {'message': 'Missing fields'}, 400

        user = User.find_by_username(username)
        if not user:
            return {'message': 'User not found'}, 404

        if user['is_verified']:
            return {'message': 'User already verified'}, 400

        if user['verification_code'] != verification_code:
            return {'message': 'Invalid verification code'}, 400

        User.update(user, {
            'is_verified': True,
            'updated_at': now()
        })
        return {'message': 'User verified successfully'}, 200


class LoginWithCredentials(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Check if have all fields
        if not username or not password:
            return {'message': 'Missing fields'}, 400

        user = User.find_by_username(username)

        if not user:
            return {'message': 'User not found'}, 404

        if not user['is_verified']:
            return {'message': 'User not verified'}, 400

        if not bcrypt.check_password_hash(user['password_hash'], password):
            return {'message': 'Invalid password'}, 400

        user = User.find_by_username(username, include_keys=[
                                     '_id', 'username', 'email', 'role', 'avatar'])

        return {'message': 'Login successful', 'record': user}, 200


class UserResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.find_by_username(current_user, exclude_keys=[
                                     'password_hash', 'verification_code'])
        if not user:
            return {'message': 'User not found'}, 404
        return {'message': 'User found', 'record': user}, 200
