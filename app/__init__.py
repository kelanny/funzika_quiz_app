from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestConfig)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from app.models.base_model import BaseModel
        from app.models.user import User
        from app.models.question import Question
        from app.models.answer import Answer
        from app.models.user_answer import UserAnswer
        from app.models.quiz import Quiz

        db.create_all()
    return app

