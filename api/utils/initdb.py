from api.models.book import Book
from api.models.page import Page
from api.utils.time import now
from api.utils.db import db
from flask import current_app as app
import os
import pymongo

def initialize_data():
        list_of_collections = db.list_collection_names()
        if 'books' in list_of_collections:
            db.books.drop()
            print('books dropped')
        if 'pages' in list_of_collections:
            db.pages.drop()
            print('pages dropped')
        book1 = Book(title='book1', status='submitting', created_at=now())
        book2 = Book(title='book2', status='submitting', created_at=now())
        book1.save()
        book2.save()
        image11_url = os.path.join(app.config['UPLOAD_FOLDER'], '1-1.png')
        image12_url = os.path.join(app.config['UPLOAD_FOLDER'], '1-2.png')
        image13_url = os.path.join(app.config['UPLOAD_FOLDER'], '1-3.png')
        image21_url = os.path.join(app.config['UPLOAD_FOLDER'], '2-1.png')
        image22_url = os.path.join(app.config['UPLOAD_FOLDER'], '2-2.png')
        page11 = Page(image=image11_url ,description='blue 1', creator_id='1', book_id=book1._id, created_at=now(), interval_id=1)
        page11.save()
        page12 = Page(image=image12_url ,description='blue 2', creator_id='2', book_id=book1._id, created_at=now(), interval_id=2)
        page12.save()
        page13 = Page(image=image13_url ,description='blue 3', creator_id='3', book_id=book1._id, created_at=now(), interval_id=3)
        page13.save()
        page21 = Page(image=image21_url ,description='black 1', creator_id='1', book_id=book2._id, created_at=now(), interval_id=1)
        page21.save()
        page22 = Page(image=image22_url ,description='black 2', creator_id='2', book_id=book2._id, created_at=now(), interval_id=2)
        page22.save()
        Book.push_new_page(book1._id, page11._id)
        Book.push_new_page(book1._id, page12._id)
        Book.push_new_page(book1._id, page13._id)
        Book.push_new_page(book2._id, page21._id)
        Book.push_new_page(book2._id, page22._id)
        print('Data initialized with 2 books and 5 pages!')
