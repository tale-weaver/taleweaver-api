from flask import request
from flask_restful import Resource
from api.models.book import Book
from api.models.page import Page

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
