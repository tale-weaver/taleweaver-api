
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.resources.user import Signup
from api.resources.book import allStory
from api.resources.page import pageUploadConfirm


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'tw'  # Change this!
jwt = JWTManager(app)


api.add_resource(Signup, '/user/signup')
api.add_resource(allStory, '/story')
api.add_resource(pageUploadConfirm, '/story/upload/<book_id>')

if __name__ == '__main__':
    app.run(debug=True)