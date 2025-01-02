#!/usr/bin/python3
""" Contains the User class"""
from app import db, login_manager
from flask_login import UserMixin
from app.models.base_model import BaseModel
from app.models.user_answer import UserAnswer

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(user_id)


class User(BaseModel):
    """Representation of user """
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

    # Flask-Login required methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True  # Change this if you implement user account activation

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Return the user's unique identifier
    
    def make_admin(self):
        """Change user to admin"""
        self.is_admin = True
        db.session.commit()
        return True

