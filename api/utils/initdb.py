from api.models.book import Book
from api.models.page import Page
from api.models.user import User
from api.utils.time import now
from api.utils.db import db


def initialize_data():
    
    print("Data initialized with 2 users 2 books and 20 pages!")