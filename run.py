
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.resources.book import AllStory, SingleBook
from api.resources.page import PageUploadConfirm
from flask_mail import Mail

from api.resources.user import Signup, ResendVerificationEmail, VerifyEmail, UserResource, LoginWithCredentials
from api.utils.json_encoder import MongoJSONProvider, MongoJSONEncoder
from api.config.config import Config
from api.resources.getImage import StaticImage
import os


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
app.config['JWT_SECRET_KEY'] = 'tw'  # Change this!
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'data')
jwt = JWTManager(app)

api.add_resource(StaticImage, '/data/<filename>')
api.add_resource(AllStory, '/story')
api.add_resource(PageUploadConfirm, '/story/upload/<book_id>')
api.add_resource(SingleBook, '/story/<book_id>')
api.add_resource(Signup, '/user/signup')
api.add_resource(ResendVerificationEmail, '/user/resend_verification_email')
api.add_resource(VerifyEmail, '/user/verify')
api.add_resource(LoginWithCredentials, '/user/login_with_credentials')
api.add_resource(UserResource, '/user')


if __name__ == '__main__':
    app.run()
