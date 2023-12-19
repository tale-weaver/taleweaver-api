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

from api.config.config import Config


class PageUploadConfirm(Resource):
    @jwt_required()
    def post(self, book_id):
        text_description = request.form.get("text_description")
        # creator = request.form.get("creator")
        creator = get_jwt_identity()

        file = request.files.get("file")
        filename = secure_filename(file.filename)
        images_folder = os.path.join(app.root_path, "data", creator)

        if not file:
            return {"msg": "Missing file"}, 400
        if not creator:
            return {"msg": "Missing creator"}, 400
        if not text_description:
            return {"msg": "Missing text description"}, 400
        
        filepath = os.path.join(images_folder, filename)
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        
        file.save(filepath)

        image_url = os.path.join(Config.BACKEND_URL, filename)

        creator_id = User.find_by_username(creator)["_id"]
        newPage = Page(
            image=image_url,
            description=text_description,
            creator_id=creator_id,
        )
        newPage.save()
        return {
            "msg": "success",
        }, 200

    def get(self, book_id):
        book = Book.find_by_id(book_id)
        bookname = book["title"]
        page_num = len(book["page_ids"]) + 1

        return {
            "msg": "success",
            "records": {"bookname": bookname, "page_num": page_num},
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
