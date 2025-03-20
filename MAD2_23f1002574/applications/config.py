import os
basedir= os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG=False
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI=None
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir,"../db_directory")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/suneh/MAD2_23f1002574/db_directory/household.db'
    DEBUG=True
    CELERY_BROKER_URL="redis://localhost:6379/1"
    CELERY_RESULT_BACKEND="redis://localhost:6379/2"