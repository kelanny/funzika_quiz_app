import os

basedir = os.path.abspath(os.path.dirname(__file__))    


class Config:
    # SECRET_KEY = os.environ.get('SECRET' or 'my-secret-key')
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False                            