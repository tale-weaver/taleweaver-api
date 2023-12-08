from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from api.models.page import Page
from api.models.book import Book

class pageUploadConfirm(Resource):
    def post(self):
        data = request.get_json()
        book_id = data['book_id']
        image = data['image']
        text_description = data['text_description']
        creator_id = data['creator']
        
        if not book_id or not  image or not text_description or not creator_id:
            return {'msg': 'Missing fields'}, 400

        bookname = Book.find_by_bookid(book_id)['bookname']
        newPage = Page(image=image, description=text_description, creator=creator_id)
        newPage.save()
        return {
            'msg': 'success',
            'records':{
                'bookname': bookname,
                'image': image,
                'text_description': text_description,
                'creator': Page.find_creator_by_id(creator_id)
            }
        }, 200

    def get(self):
        data = request.get_json()
        book_id = data['book_id']
        bookname = Book.find_by_bookid(book_id)['bookname']

        return {'msg': 'success',
                'records': {
                    'bookname': bookname,
                }}, 200