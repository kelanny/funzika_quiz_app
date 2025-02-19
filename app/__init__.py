from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
import os


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app(config=None):
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
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'info'

    # Initialize migration
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.quiz.routes import quiz_bp
    from app.question.routes import questions_bp
    from app.user.routes import user_bp
    from app.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp, url_prefix='/quizzes')
    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(user_bp)

    # Register CLI commands
    from app.quiz.cli import quiz_cli
    from app.question.cli import question_cli
    from app.user.cli import user_cli
    from app.answer.cli import answer_cli
    from app.user_answer.cli import user_answer_cli
    from app.commands import populate_cli

    app.cli.add_command(quiz_cli)
    app.cli.add_command(question_cli)
    app.cli.add_command(user_cli)
    app.cli.add_command(answer_cli)
    app.cli.add_command(user_answer_cli)
    app.cli.add_command(populate_cli)

    with app.app_context():
        from app.models.base_model import BaseModel
        from app.user.models import User
        from app.quiz.models import Quiz
        from app.question.models import Question
        from app.answer.models import Answer
        from app.user_answer.models import UserAnswer
  
    return app
