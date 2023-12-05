
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.resources.user import Signup

app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'tw'  # Change this!
jwt = JWTManager(app)


api.add_resource(Signup, '/user/signup')


if __name__ == '__main__':
    app.run(debug=True)