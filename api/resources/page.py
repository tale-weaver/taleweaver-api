from flask import request
from flask import current_app as app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from api.models.page import Page
from api.models.book import Book
from api.models.user import User
from api.utils.time import now
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

from urllib.parse import urljoin

from api.config.config import Config


class PageUploadConfirm(Resource):
    @jwt_required()
    def post(self, book_id):
        text_description = request.form.get("text_description")
        creator = get_jwt_identity()
        _file = request.files.get("file")

        if not _file or not text_description or not creator:
            return {"msg": "Missing fields"}, 400

        user = User.find_by_username(creator)

        if not user:
            return {"msg": "User does not exist"}, 400

        images_folder = os.path.join(
            app.root_path, Config.STATIC_FOLDER, str(user["_id"]))

        filename = secure_filename(_file.filename)
        filepath = os.path.join(images_folder, filename)

        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        _file.save(filepath)

        image_url = urljoin(Config.BACKEND_URL, filepath.replace(
            app.root_path, "").replace("\\", "/"))
        newPage = Page(
            image=image_url,
            description=text_description,
            creator_id=user["_id"],
        )
        newPage.save()

        # add page to book
        page = Page.find_by_path(image_url)
        Book.push_new_page(book_id, page["_id"])

        return {"msg": "success upload page"}, 200

    def get(self, book_id):
        book = Book.find_by_id(book_id)
        bookname = book["title"]
        winner_page_num = len(Book.find_winner_pages(book_id))

        return {
            "msg": "success",
            "records": {"bookname": bookname, "page_num": winner_page_num+1},
        }, 200


class VotePage(Resource):
    @jwt_required()
    def post(self, page_id):
        username = get_jwt_identity()

        if not username:
            return {"msg": "Missing username"}, 400

        user = User.find_by_username(username)

        success = Page.voted_by_user(page_id, user["_id"])
        if not success:
            return {"msg": "You have already voted this page"}, 400

        return {"msg": "You vote this page successfully"}, 200


class UnVotePage(Resource):
    @jwt_required()
    def post(self, page_id):
        username = get_jwt_identity()

        if not username:
            return {"msg": "Missing username"}, 400

        user = User.find_by_username(username)

        success = Page.voted_by_user(page_id, user["_id"], unvote=True)
        if not success:
            return {"msg": "You have not voted this page"}, 400

        return {"msg": "You unvote this page successfully"}, 200
