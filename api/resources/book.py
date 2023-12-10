from flask import request, url_for
from flask_restful import Resource
from flask import current_app as app
from api.models.book import Book
from api.models.page import Page
from werkzeug.utils import secure_filename

class allStory(Resource):
    def get(self):
        all_books = Book.find_all_books()
        if not all_books:
            return {'msg': 'No books'}
        formatted_books = []
        for book in all_books:
            bookurl = Page.find_cover_by_bookid(book['_id'])
            formatted_book = {
                'bookurl': bookurl,
                'bookname': book['bookname'],
                'numlikes': book['like'],
                'numcomments': len(book['comment']),
                'state': book['status'],
                'date': book['create_date']
            }
            formatted_books.append(formatted_book)

        return {'msg': 'success',
                'records': formatted_books}, 200

    def post(self):
        data = request.get_json()
        bookname = data['bookname']
        text_description = data['text_description']
        creator_id = data['creator']
        
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image_url = url_for('static', filename='uploads/' + file.filename, _external=True)

        newBook = Book(status='submitting', title=bookname)
        newBook.save()
        newPage = Page(image=image_url, description=text_description, creator=creator_id, book_id=newBook['_id'])
        newPage.save()
        Book.push_new_page(book_id, newPage['_id'])

        page_num = len(book['page_ids'])
        return {'msg': 'success',
                'records': {
                    'bookname': bookname,
                    'image': image_url,
                    'page_num': page_num
                }}, 200