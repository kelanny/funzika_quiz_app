#!/usr/bin/python3
""" Contains the User class"""
from app import db, login_manager
from flask_login import UserMixin
from app.base_model import BaseModel
from app.user_answer.models import UserAnswer


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(user_id)


class User(BaseModel):
    """Representation of user

    Attributes:
        - username (str): A string representing username
        - email (str): A string representing email
        - password_hash (str): A string representing hashed password

    Methods:

    """
    __tablename__ = 'users'

    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)

    user_answers = db.relationship('UserAnswer', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password_hash, is_admin=False):
        """Initialize the user"""
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'is_admin': self.is_admin,
            'user_answers': self.user_answers
        })

    # Flask-Login required methods
    @property
    def is_authenticated(self):
        """Check if user is authenticated"""
        return True

    @property
    def is_active(self):
        """Checks if user is active"""
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Returns the user's unique identifier"""
        return str(self.id)

    def make_admin(self):
        """Change user to admin"""
        self.is_admin = True
        db.session.commit()
        return True
