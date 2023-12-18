
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from api.resources.user import Signup, ResendVerificationEmail, VerifyEmail, UserResource, LoginWithCredentials
from api.resources.book import AllStory, SingleBook, LikeBook
from api.resources.page import PageUploadConfirm, VotePage
from api.resources.comment import AddComment
from api.resources.getImage import StaticImage

from api.utils.init_db import db_init
from api.utils.json_encoder import MongoJSONEncoder
from api.config.config import Config


app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
CORS(app)
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

mail = Mail()
mail.init_app(app)
JWTManager(app)

api = Api(app)

api.add_resource(StaticImage, '/data/<filename>')
api.add_resource(AllStory, '/story')
api.add_resource(PageUploadConfirm, '/story/upload/<book_id>')
api.add_resource(SingleBook, '/story/<book_id>')
api.add_resource(VotePage, '/story/<page_id>/vote')
api.add_resource(LikeBook, '/story/<book_id>/like')
api.add_resource(Signup, '/user/signup')
api.add_resource(ResendVerificationEmail, '/user/resend_verification_email')
api.add_resource(VerifyEmail, '/user/verify')
api.add_resource(LoginWithCredentials, '/user/login_with_credentials')
api.add_resource(UserResource, '/user')
api.add_resource(AddComment, '/story/<book_id>/comment')

if __name__ == '__main__':
    with app.app_context():
        db_init()

    app.run()
