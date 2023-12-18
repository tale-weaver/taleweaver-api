from flask import request
from flask_restful import Resource
from flask import current_app as app
from api.models.book import Book
from api.models.page import Page
from api.models.user import User
from api.models.comment import Comment
from werkzeug.utils import secure_filename
from api.utils.time import now
from bson import ObjectId
import os
from flask_jwt_extended import jwt_required, get_jwt_identity


class AllStory(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.find_by_username(username)
        user_liked_book_ids = user["liked_book_ids"]
        all_books = Book.find_all_books()
        if not all_books:
            return {"msg": "No books"}, 400
        formatted_books = []

        for book in all_books:
            num_likes = len(book["liked_by_user_ids"])
            num_comments = len(book["comment_ids"])

            liked = False
            if book["_id"] in user_liked_book_ids:
                liked = True

            formatted_book = {
                "bookurl": book["cover"],
                "bookname": book["title"],
                "book_id": book["_id"],
                "liked": liked,
                "numlikes": num_likes,
                "numcomments": num_comments,
                "state": book["status"],
                "date": book["created_at"],
            }
            formatted_books.append(formatted_book)

        return {"msg": "success", "records": formatted_books}, 200


class SingleBook(Resource):
    def get(self, book_id):
        if book_id is None:
            return {"msg": "Missing story fields"}, 400
        book = Book.find_by_id(book_id)
        if not book:
            return {"msg": "No book"}, 400

        page_num = len(book["page_ids"])
        num_likes = len(book["liked_by_user_ids"])
        num_comments = len(book["comment_ids"])
        status = book["status"]
        pages_winner = Book.find_winner_pages(book_id)
        if status == "voting" or "submitting":
            pages_status = Page.find_pages_by_bookid(book_id)
        elif status == "finished":
            pages_status = {}
        comments = Comment.find_comment_of_book(book_id)
        formatted_book = {
            "bookurl": book["cover"],
            "bookname": book["title"],
            "numlikes": num_likes,
            "numcomments": num_comments,
            "state": status,
            "pages": {"winner": pages_winner, "ongoning": pages_status},
            "page_num": page_num + 1,
            "comments": comments,
        }
        return {"msg": "success", "records": formatted_book}, 200


class LikeBook(Resource):
    @jwt_required()
    def post(self, book_id):
        username = get_jwt_identity()
        # data = request.get_json()
        # username = data["username"]
        if not username:
            return {"msg": "Missing username"}, 400
        Book.liked_by_user(book_id, username)

        book_oid = ObjectId(book_id)
        user = User.find_by_username(username)
        user_liked_book_ids = user["liked_book_ids"]
        if book_oid not in user_liked_book_ids:
            user_liked_book_ids.append(book_oid)
        else:
            user_liked_book_ids.remove(book_oid)

        book = Book.find_by_id(book_id)
        numlikes = len(book["liked_by_user_ids"])
        return {"msg": "success", "records": {"numlikes": numlikes}}, 200


class CreateBook(Resource):
    def post(self):
        bookname = request.form.get("bookname")
        text_description = request.form.get("text_description")
        creator_id = "TaleWeaver"
        file = request.files.get("file")
        filename = secure_filename(file.filename)
        images_folder = os.path.join(app.root_path, "data")
        os.makedirs(images_folder, exist_ok=True)

        filepath = os.path.join(images_folder, filename)
        file.save(filepath)

        image_url = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        newBook = Book(status="submitting", title=bookname, created_at=now())
        newBook.save()
        newPage = Page(
            image=image_url,
            description=text_description,
            creator_id=creator_id,
            book_id=newBook._id,
            created_at=now(),
            interval_id=1,
        )
        newPage.save()
        Book.push_new_page(newBook._id, newPage._id)

        page_num = len(newBook.page_ids)
        return {
            "msg": "success",
            "records": {"bookname": bookname, "image": image_url, "page_num": page_num},
        }, 200


class TestFunction(Resource):
    def get(self, book_id):
        book = Book.find_by_id(book_id)
        pages = Page.find_pages_by_bookid(book_id, book["status"])
        return {"msg": "success", "records": {"pages": pages}}, 200

