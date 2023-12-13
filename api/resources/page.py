from flask import request
from flask import current_app as app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from api.models.page import Page
from api.models.book import Book
from api.models.user import User
from api.utils.time import now
import os


class PageUploadConfirm(Resource):
    def post(self, book_id):
        # book_id = request.args.get('book_id')
        print("book_id: " + str(book_id))
        text_description = request.form.get("text_description")
        creator = request.form.get("creator")

        file = request.files.get("file")
        filename = secure_filename(file.filename)
        images_folder = os.path.join(app.root_path, "data")
        print("text_description: " + str(text_description))
        print("creator: " + str(creator))
        if not file:
            return {"msg": "Missing file"}, 400
        if not creator:
            return {"msg": "Missing creator"}, 400
        if not text_description:
            return {"msg": "Missing text description"}, 400
        filepath = os.path.join(images_folder, filename)
        print(filepath)
        file.save(filepath)

        image_url = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        creator_id = User.find_by_username(creator)["_id"]
        newPage = Page(
            image=image_url,
            description=text_description,
            creator_id=creator_id,
            book_id=book_id,
            created_at=now(),
            interval_id=1,
        )
        newPage.save()

        book = Book.find_by_bookid(book_id)
        bookname = book["title"]

        return {
            "msg": "success",
            "records": {
                "bookname": bookname,
                "image": image_url,
                "text_description": text_description,
                "creator": creator,
            },
        }, 200

    def get(self, book_id):
        book = Book.find_by_bookid(book_id)
        bookname = book["title"]
        page_num = len(book["page_ids"]) + 1

        return {
            "msg": "success",
            "records": {"bookname": bookname, "page_num": page_num},
        }, 200


class VotePage(Resource):
    def post(self, page_id):
        data = request.get_json()
        username = data["username"]
        if not username:
            return {"msg": "Missing username"}, 400
        user = User.find_by_username(username, include_keys=["_id"])
        user_id = user["_id"]
        print('this is user_id in VotePage:')
        print(user_id)
        page = Page.voted_by_user(page_id, user_id)
        print(page['voted_by_user_ids'])
        numvotes = len(page['voted_by_user_ids'])+1
        return {"msg": "success", "records": {"numvotes": numvotes}}, 200
