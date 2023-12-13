from api.models.book import Book
from api.models.page import Page
from api.utils.time import now
from api.utils.db import db
from flask import current_app as app
import os


def initialize_data():
    list_of_collections = db.list_collection_names()
    if "books" in list_of_collections:
        db.books.drop()
        print("books dropped")
    if "pages" in list_of_collections:
        db.pages.drop()
        print("pages dropped")
    like_list_1 = ["user1", "user2", "user3"]
    like_list_2 = []
    book1 = Book(title="book1", status="submitting", created_at=now(), liked_by_user_ids=like_list_1)
    book2 = Book(title="book2", status="submitting", created_at=now(), liked_by_user_ids=like_list_2)
    book1.save()
    book2.save()
    image11_url = os.path.join(app.config["UPLOAD_FOLDER"], "1-1.png")
    image12_url = os.path.join(app.config["UPLOAD_FOLDER"], "1-2.png")
    image13_url = os.path.join(app.config["UPLOAD_FOLDER"], "1-3.png")
    image21_url = os.path.join(app.config["UPLOAD_FOLDER"], "2-1.png")
    image22_url = os.path.join(app.config["UPLOAD_FOLDER"], "2-2.png")
    vote_list_11 = ["user1", "user2", "user3"]
    vote_list_12 = ["user1", "user2", "user3", "user4", "user5", "user6"]
    vote_list_13 = ["user1"]
    vote_list_21 = ["user1", "user2", "user3"]
    vote_list_22 = ["user1", "user2", "user3", "user4"]
    page11 = Page(
        image=image11_url,
        description="blue 1",
        creator_id="1",
        book_id=book1._id,
        created_at=now(),
        interval_id=1,
        status="winner",
        voted_by_user_ids=vote_list_11,
    )
    page11.save()
    page12 = Page(
        image=image12_url,
        description="blue 2",
        creator_id="2",
        book_id=book1._id,
        created_at=now(),
        interval_id=2,
        status="winner",
        voted_by_user_ids=vote_list_12,
    )
    page12.save()
    page13 = Page(
        image=image13_url,
        description="blue 3",
        creator_id="3",
        book_id=book1._id,
        created_at=now(),
        interval_id=3,
        status="ongoing",
        voted_by_user_ids=vote_list_13,
    )
    page13.save()
    page21 = Page(
        image=image21_url,
        description="black 1",
        creator_id="1",
        book_id=book2._id,
        created_at=now(),
        interval_id=9,
        status="winner",
        voted_by_user_ids=vote_list_21,
    )
    page21.save()
    page22 = Page(
        image=image22_url,
        description="black 2",
        creator_id="2",
        book_id=book2._id,
        created_at=now(),
        interval_id=10,
        status="ongoing",
        voted_by_user_ids=vote_list_22,
    )
    page22.save()
    Book.push_new_page(book1._id, page11._id)
    Book.push_new_page(book1._id, page12._id)
    Book.push_new_page(book1._id, page13._id)
    Book.push_new_page(book2._id, page21._id)
    Book.push_new_page(book2._id, page22._id)
    print("Data initialized with 2 books and 5 pages!")
