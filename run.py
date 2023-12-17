
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.resources.book import AllStory, SingleBook, LikeBook
from api.resources.page import PageUploadConfirm, VotePage
from api.resources.comment import AddComment
from flask_mail import Mail

from api.resources.user import Signup, ResendVerificationEmail, VerifyEmail, UserResource, LoginWithCredentials
from api.utils.json_encoder import MongoJSONEncoder
from api.config.config import Config
from api.resources.getImage import StaticImage
from api.utils.initdb import initialize_data
import os


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
# app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'data')
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
api.add_resource(AddComment,'/story/<book_id>/comment')

from apscheduler.schedulers.background import BackgroundScheduler
from api.models.book import Book
from api.models.page import Page
from api.utils.time import now

scheduler = BackgroundScheduler()
scheduler.start()

# find all submitting books -> 
# if book has less than 9 pages -> update book status to voting
# if book  9 pages -> update book status to finished

# find all voting books ->
# if book has less than 9 pages -> update book status to submitting
# choose winner page -> update page status to winner -> update


# update book current interval id
def check_book_status():
    print("start check_book_status")
    books_submitting = Book.find_all_books_by_status("submitting")
    books_voting = Book.find_all_books_by_status("voting")
    if books_submitting is None and books_voting is None:
        print("no book")
        return
    elif books_submitting is None:
        for book in books_voting:
            if book["current_interval_id"] <= now() and len(book["page_ids"]) < 8:
                Book.update_book_status(book["_id"], "submitting")
                print(book["title"] + "update to submitting")
            elif book["current_interval_id"] <= now() and len(book["page_ids"]) == 8:
                Book.update_book_status(book["_id"], "finished")
                print(book["title"] + "update to finished")
                # push winner page into book
            pages_voting = Page.find_voting_pages(book["_id"])
            for page in pages_voting:
                max_vote = 0
                if len(page["voted_by_user_ids"]) >= max_vote:
                    max_vote = page["voted_by_user_ids"]
                    winner_page = page
                    print(winner_page["_id"] + "is winner")
            for page in pages_voting:
                if page["_id"] != winner_page["_id"]:
                    Page.update_status_as_loser(page["_id"])
                    print(page["_id"] + "is loser")
                else:
                    Page.update_status_as_winner(page["_id"])
                    print(page["_id"] + "is winner")
    elif books_voting is None:
        for book in books_submitting:
            if book["current_interval_id"] <= now():
                Book.update_book_status(book["_id"], "voting")        
                print(book["title"]+"update to voting")

    Book.push_new_page(book["_id"], winner_page["_id"])
    Book.update_current_interval_id(book["_id"])
    print("end check_book_status")

scheduler.add_job(check_book_status, 'interval', seconds=5)
if __name__ == '__main__':
    with app.app_context():
        initialize_data()

        # creator = "TaleWeaver"
        # file_name = "test.jpg"
        # file_path_local = os.path.join(app.root_path, "data", creator, file_name)

        # img_url = os.path.join(Config.BACKEND_URL, "data", creator, file_name)

    app.run()
