import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","abdelfatah_secret_key")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
