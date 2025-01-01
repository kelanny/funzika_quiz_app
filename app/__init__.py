from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
import os


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'testing':
        app.config.from_object('config.TestingConfig')
    elif env == 'production':
        app.config.from_object('config.ProdConfig')
    elif env == 'development':
        app.config.from_object('config.DevConfig')
    else:
        raise ValueError('FLASK_ENV not set properly')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    # Initialize migration
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes.quiz_routes import quiz_blueprint
    from app.routes.user_routes import users

    app.register_blueprint(quiz_blueprint, url_prefix='/quizzes')
    app.register_blueprint(users)

    with app.app_context():
        from app.models.base_model import BaseModel
        from app.models.user import User
        from app.models.quiz import Quiz
        from app.models.question import Question
        from app.models.answer import Answer
        from app.models.user_answer import UserAnswer
  
    return app

