from flask import request
from flask import current_app as app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from api.models.page import Page
from api.models.book import Book
from api.utils.time import now
import os

class PageUploadConfirm(Resource):
    def post(self):

        book_id = request.form.get('book_id')
        text_description = request.form.get('test_description')
        creator_id = request.form.get('creator')
        
        file = request.files['file']
        if not book_id or not file or not text_description or not creator_id:
            return {'msg': 'Missing fields'}, 400

        bookname = Book.find_by_bookid(book_id)['bookname']
        # modify the path to save the image
        
        filename = secure_filename(file.filename)
        image_url = f'http://localhost:5000/static/uploads/{filename}'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        newPage = Page(image=image_url, description=text_description, creator_id=creator_id, book_id=book_id, created_at=now())
        newPage.save()
        creator = Page.find_creator_by_id(creator_id)
        return {
            'msg': 'success',
            'records':{
                'bookname': bookname,
                'image': image_url,
                'text_description': text_description,
                'creator': creator
            }
        }, 200

    def get(self):
        data = request.get_json()
        book_id = data['book_id']
        book = Book.find_by_bookid(book_id)
        bookname = book['bookname']
        page_num = len(book['page_ids'])

        return {'msg': 'success',
                'records': {
                    'bookname': bookname,
                    'page_num': page_num
                }}, 200