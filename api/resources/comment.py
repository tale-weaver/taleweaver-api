from flask import request
from flask_restful import Resource
from api.models.user import User
from api.models.book import Book
from api.models.comment import Comment
from flask_bcrypt import Bcrypt
from api.utils.time import now
import random
from flask_jwt_extended import jwt_required, get_jwt_identity


bcrypt = Bcrypt()

class AddComment(Resource):
    # @jwt_required()
    def post(self,book_id):
        data = request.get_json()
        content = data['content']
        # username = get_jwt_identity()
        # user = User.find_by_username(username, include_keys=["_id"])
        # commenter = user["_id"]
        print(data)
        if not content:
            return {"msg": "Missing content"}, 400
        # if not commenter:
        #     return {"msg": "Missing commenter"}, 400
        # commenter_id = User.find_by_username(commenter)["_id"]
        newComment=Comment(
            # commenter_id=commenter_id
            commenter_id=0,
            content=content,
            created_at=now(),
            updated_at=now(),
        )
        newComment.save()
        book=Book.push_comment(book_id,newComment._id)
        print(book)
        print(len(book["comment_ids"]))
        print(newComment._id)
        numComments=len(book["comment_ids"])
        
        return {
            "msg": "success",
            "records": {"username": 0, "content": content, "created_at": newComment.created_at,"numComments":numComments},
        }, 200
