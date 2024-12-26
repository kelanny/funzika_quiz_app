#!/usr/bin/python3
""" Contains the Quiz class"""
from app import db 
from app.models.base_model import BaseModel



class Quiz(BaseModel, db.Model):
    """Representation of quiz """
    __tablename__ = 'quizzes'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.TEXT)
    is_active = db.Column(db.Boolean)

    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __init__(self, title, description, is_active=False):
        """Instantiates a new quiz"""
        super().__init__()
        self.title = title
        self.description = description
        self.is_active = is_active
    

