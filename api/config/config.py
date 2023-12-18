import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URL = os.getenv('MONGO_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MAIL_SENDER = os.getenv('MAIL_SENDER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    BACKEND_URL = "http://127.0.0.1:5000"
    INTERVAL_TIME = 30
    STATIC_FOLDER = 'bin'

    print(f"The BACKEND_URL is {BACKEND_URL}")
