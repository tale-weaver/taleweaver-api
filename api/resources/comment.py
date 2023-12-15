from flask import request
from flask_restful import Resource
from api.models.user import User
from api.models.book import Book
from api.models.comment import Comment
from flask_bcrypt import Bcrypt
from api.utils.time import now
import random

bcrypt = Bcrypt()

class AddComment(Resource):
    def post(self,book_id):
        data = request.get_json()
        content = data['content']
        commenter = data['commenter']
        # content = request.form.get("content")
        # commenter = request.form.get("commenter")
        print(data)
        if not content:
            return {"msg": "Missing content"}, 400
        if not commenter:
            return {"msg": "Missing commenter"}, 400
        commenter_id = User.find_by_username(commenter)["_id"]

        newComment=Comment(
            commenter_id=0,
            content=content,
            created_at=now(),
            updated_at=now(),
        )
        newComment.save()
        book=Book.add_comment_id(book_id,newComment._id)
        print(book)
        print(newComment._id)
        numComments=len(book["comment_ids"])
        
        return {
            "msg": "success",
            "records": {"username": commenter, "content": content, "created_at": newComment.created_at,"numComments":numComments},
        }, 200
