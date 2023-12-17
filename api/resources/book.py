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
    def get(self):
        all_books = Book.find_all_books()
        if not all_books:
            return {"msg": "No books"}, 400
        formatted_books = []

        for order, book in enumerate(all_books, start=1):
            bookurl = Page.find_cover_by_bookid(book["_id"])
            numlikes = len(book["liked_by_user_ids"])
            numcomments = len(book["comment_ids"])
            formatted_book = {
                "bookurl": bookurl,
                "bookname": book["title"],
                "book_id": order,
                "numlikes": numlikes,
                "numcomments": numcomments,
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
        bookname = book["title"]
        page_num = len(book["page_ids"])
        numlikes = len(book["liked_by_user_ids"])
        numcomments = len(book["comment_ids"])
        state = book["status"]
        pages = Page.find_pages_by_bookid(book_id)
        pages_voting = Page.find_voting_pages(book_id)
        comments= Comment.find_comment_of_book(book_id)
        formatted_book = {
            "bookname": bookname,
            "numlikes": numlikes,
            "numcomments": numcomments,
            "state": state,
            "pages": pages,
            "pages_voting": pages_voting,
            # 狀態下的頁面是否包含投票中？
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


class SingleBook(Resource):
    def get(self, book_id):
        if book_id is None:
            return {"msg": "Missing story fields"}, 400
        book = Book.find_by_id(book_id)
        if not book:
            return {"msg": "No book"}, 400
        bookname = book["bookname"]
        page_num = len(book["page_ids"])
        numlikes = len(book["liked_by_user_ids"])
        numcomments = len(book["comment_ids"])
        state = book["status"]
        pages = Page.find_pages_by_bookid(book_id)
        pages_voting = Page.find_voting_pages(book_id)
        formatted_book = {
            "bookname": bookname,
            "numlikes": numlikes,
            "numcomments": numcomments,
            "state": state,
            "pages": pages,
            # 狀態下的頁面是否包含投票中？
            "pages_voting": pages_voting,
            "page_num": page_num,
        }
        return {"msg": "success", "records": formatted_book}, 200