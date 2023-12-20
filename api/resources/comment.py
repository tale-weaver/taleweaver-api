from flask import request
from flask_restful import Resource
from api.models.user import User
from api.models.book import Book
from api.models.comment import Comment
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity


bcrypt = Bcrypt()


class AddComment(Resource):
    @jwt_required()
    def post(self, book_id):
        data = request.get_json()
        review = data['review']
        rating = data['rating']
        username = get_jwt_identity()
        user = User.find_by_username(username, include_keys=["_id"])
        commenter_id = user["_id"]
        print(data)
        if not rating:
            return {"msg": "Missing rating"}, 400
        if not review:
            return {"msg": "Missing review"}, 400
        if not commenter_id:
            return {"msg": "Missing commenter"}, 400
        newComment = Comment(
            commenter_id=commenter_id,
            review=review,
            rating=rating,
        )
        newComment.save()
        book = Book.push_comment(book_id, newComment._id, commenter_id)
        # print(book)
        # print(len(book["comment_ids"]))
        # print(newComment._id)
        numComments = len(book["comment_ids"])
        avatar = User.find_by_username(username)["avatar"]
        return {
            "msg": "success",
            "records": {"username": username, "review": review, "rating": rating, "avatar": avatar, "created_at": newComment.created_at, "numComments": numComments},
        }, 200
