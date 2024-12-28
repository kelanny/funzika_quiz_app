from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestConfig)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.landing_routes import landing_blueprint
    from app.routes.quiz_routes import quiz_blueprint
    from app.routes.user_routes import users_blueprint

    app.register_blueprint(landing_blueprint)
    app.register_blueprint(quiz_blueprint, url_prefix='/quizzes')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    with app.app_context():
        from app.models.base_model import BaseModel
        from app.models.user import User
        from app.models.question import Question
        from app.models.answer import Answer
        from app.models.user_answer import UserAnswer
        from app.models.quiz import Quiz

        db.create_all()
    return app

