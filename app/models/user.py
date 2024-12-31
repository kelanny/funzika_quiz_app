#!/usr/bin/python3
""" Contains the User class"""
from app import db, login_manager
from flask_login import UserMixin
from app.models.base_model import BaseModel
from app.models.user_answer import UserAnswer
from app.models.admin import Admin

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
    admin = db.relationship('Admin', backref='user', lazy=True)

    # def __init__(self, username, email, password=None):
    #     super().__init__()
    #     self.username = username
    #     self.email = email
    #     if password:
    #         self.set_password(password)
    
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
