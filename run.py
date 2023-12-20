from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_apscheduler import APScheduler

from api.resources.user import Signup, ResendVerificationEmail, VerifyEmail, UserResource, LoginWithCredentials, Subscribe, ProfileData
from api.resources.book import AllStory, SingleBook, LikeBook, TestFunction
from api.resources.page import PageUploadConfirm, VotePage
from api.resources.comment import AddComment

# from api.utils.init_db import db_init
from api.utils._init_db import db_init
from api.utils.json_encoder import MongoJSONEncoder
from api.utils.status_checker import check_book_status

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

# user related apis
api.add_resource(Signup, '/user/signup')
api.add_resource(ResendVerificationEmail, '/user/resend_verification_email')
api.add_resource(VerifyEmail, '/user/verify')
api.add_resource(LoginWithCredentials, '/user/login_with_credentials')
api.add_resource(UserResource, '/user')
api.add_resource(Subscribe, '/user/subscribe')
api.add_resource(ProfileData, '/user/profile')

# story / book related apis
api.add_resource(AllStory, '/story')
api.add_resource(PageUploadConfirm, '/story/upload/<book_id>')
api.add_resource(SingleBook, '/story/<book_id>')
api.add_resource(VotePage, '/story/<page_id>/vote')
api.add_resource(LikeBook, '/story/<book_id>/like')
api.add_resource(AddComment, '/story/<book_id>/comment')

# test
api.add_resource(TestFunction, '/test/<book_id>')


scheduler = APScheduler()


@scheduler.task('interval', id='my_task', seconds=3)
def check_status():
    check_book_status()


if __name__ == '__main__':

    with app.app_context():
        # pass
        db_init()
    scheduler.start()
    app.run()
