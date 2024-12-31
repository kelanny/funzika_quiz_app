from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
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

