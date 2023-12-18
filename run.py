from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

# from apscheduler.schedulers.background import BackgroundScheduler

from api.resources.user import Signup, ResendVerificationEmail, VerifyEmail, UserResource, LoginWithCredentials
from api.resources.book import AllStory, SingleBook, LikeBook, TestFunction
from api.resources.page import PageUploadConfirm, VotePage
from api.resources.comment import AddComment

from api.utils.init_db import db_init
from api.utils.json_encoder import MongoJSONEncoder
from api.utils.time import now, find_surrounding_datetime_indices

from api.models.page import Page
from api.models.book import Book

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

api.add_resource(TestFunction, '/test/<book_id>')
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


# scheduler = BackgroundScheduler()
# scheduler.start()

# find all submitting books ->
# if book has less than 9 pages -> update book status to voting
# if book  9 pages -> update book status to finished

# find all voting books ->
# if book has less than 9 pages -> update book status to submitting
# choose winner page -> update page status to winner -> update


from flask_apscheduler import APScheduler
aps = APScheduler()

# update book current interval id
def check_book_status():
    print("start check_book_status")
    books = Book.find_all_books()

    for book in books:

        if target_status == "finished":
            continue

        interval_ids = [book["interval_ids"] for book in books]
        timestrs = [interval["time_stamp"] for interval in interval_ids]
        target_idx_pre, target_idx_post = find_surrounding_datetime_indices(timestrs)
        target_status = interval_ids[target_idx_pre]['status']
        next_status = interval_ids[target_idx_post]['status']
        target_round = interval_ids[target_idx_pre]['round']
        next_round = interval_ids[target_idx_post]['round']
        
        

        # book information not equal to target status means it goes to next level            
        if target_status == "voting" and target_status != book["status"]:
            pages = Page.find_voting_pages(book["_id"])

            for page in pages:
                max_vote = 0
                Page.update_status(page, "loser")
                if len(page["voted_by_user_ids"]) >= max_vote:
                    max_vote = len(page["voted_by_user_ids"])
                    winner_page_id = page['_id']
            
            winner_page = Page.find_by_id(winner_page_id)
            Page.update_status(winner_page, "winner")

            winner_pages = book["page_ids"]
            winner_pages.append(winner_page_id)      
            update_dict = {"page_ids": winner_pages, "status": next_status, "round": next_round}
            Book.update(book, update_dict)
            
            print(book["title"] + "update to "+ book["status"]+ "supposed to be "+ next_status)

        elif target_status == "submitting" and target_status != book["status"]:
            update_dict = {"status": next_status, "round": next_round}
            Book.update(book, update_dict)
            
            print(book["title"] + "update to "+ book["status"]+ "supposed to be "+ next_status)


# scheduler.add_job(check_book_status, 'interval', seconds=5)
if __name__ == '__main__':
    with app.app_context():
        db_init()

    app.run()
