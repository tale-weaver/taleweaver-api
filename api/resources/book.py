from flask import request, url_for, send_from_directory
from flask_restful import Resource
from flask import current_app as app
from api.models.book import Book
from api.models.page import Page
from werkzeug.utils import secure_filename
from api.utils.time import now
import os

class AllStory(Resource):
    def get(self):
        all_books = Book.find_all_books()
        if not all_books:
            return {'msg': 'No books'}, 400
        formatted_books = []
        for book in all_books:
            bookurl = Page.find_cover_by_bookid(book['_id'])
            numlikes = len(book['liked_by_user_ids'])
            numcomments = len(book['comment_ids'])
            formatted_book = {
                'bookurl': bookurl,
                'bookname': book['bookname'],
                'numlikes': numlikes,
                'numcomments': numcomments,
                'state': book['status'],
                'date': book['created_at']
            }
            formatted_books.append(formatted_book)

        return {'msg': 'success',
                'records': formatted_books}, 200

    def post(self):
        bookname = request.form.get('bookname')
        text_description = request.form.get('text_description')
        creator_id = request.form.get('creator')
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Create the 'images' directory if it doesn't exist
        images_folder = os.path.join(app.root_path, 'data')
        os.makedirs(images_folder, exist_ok=True)

        # Update the file path to use the 'images' directory
        filepath = os.path.join(images_folder, filename)
        print(filepath)
        file.save(filepath)
        
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        newBook = Book(status='submitting', title=bookname, created_at=now()) 
        newBook.save()
        newPage = Page(image=image_url, description=text_description, creator_id=creator_id, book_id=newBook._id, created_at=now(), interval_id=1)
        newPage.save()
        Book.push_new_page(newBook._id, newPage._id)

        page_num = len(newBook.page_ids)
        return {'msg': 'success',
                'records': {
                    'bookname': bookname,
                    'image': image_url,
                    'page_num': page_num
                }}, 200
    
class SingleBook(Resource):
    def get(self):
        book_id = request.args.get('story_id', default=None, type=str)
        if book_id is None:
            return {'msg': 'Missing story fields'}, 400
        book = Book.find_by_bookid(book_id)
        if not book:
            return {'msg': 'No book'}, 400
        bookname = book['bookname']
        page_num = len(book['page_ids'])
        numlikes = len(book['liked_by_user_ids'])
        numcomments = len(book['comment_ids'])
        state = book['status']
        pages = Page.find_pages_by_bookid(book_id)
        formatted_book = {
            'bookname': bookname,
            'numlikes': numlikes,
            'numcomments': numcomments,
            'state': state,
            'pages': pages,
            # 狀態下的頁面是否包含投票中？
            'page_num': page_num
        }
        return {'msg': 'success',
                'records': formatted_book}, 200