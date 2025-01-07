import os
from dotenv import load_dotenv
from os import getenv

basedir = os.path.abspath(os.path.dirname(__file__))    

load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable the modification tracker

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    # 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    #     getenv('MYSQL_DEV_USER'),
    #     getenv('MYSQL_DEV_PASSWORD'),
    #     getenv('MYSQL_DEV_HOST'),
    #     getenv('MYSQL_DEV_PORT'),
    #     getenv('MYSQL_DEV_DB')
    # )
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'your_csrf_secret_key'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        getenv('MYSQL_TEST_USER'),
        getenv('MYSQL_TEST_PASSWORD'),
        getenv('MYSQL_TEST_HOST'),
        getenv('MYSQL_TEST_PORT'),
        getenv('MYSQL_TEST_DB')
    )                      
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        getenv('MYSQL_PROD_USER'),
        getenv('MYSQL_PROD_PASSWORD'),
        getenv('MYSQL_PROD_HOST'),
        getenv('MYSQL_PROD_PORT'),
        getenv('MYSQL_PROD_DB')
    )
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'your_csrf_secret_key'
