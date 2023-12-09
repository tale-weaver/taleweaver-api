
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from api.resources.user import Signup, UserResource
from api.utils.json_encoder import MongoJSONProvider, MongoJSONEncoder
from api.config.config import Config


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['RESTFUL_JSON'] = {'cls': MongoJSONEncoder}
app.config.update(
    DEBUG=False,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('Tale Weaver', Config.MAIL_SENDER),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD
)
# app.json = MongoJSONProvider(app)

mail = Mail()
mail.init_app(app)
JWTManager(app)

api = Api(app)
api.add_resource(Signup, '/user/signup')
api.add_resource(UserResource, '/user/<username>')


if __name__ == '__main__':
    app.run()
