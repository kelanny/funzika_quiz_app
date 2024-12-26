#!/usr/bin/python3
""" Contains the Question class """
from app.models.base_model import BaseModel
from app import db


class Question(BaseModel):
    """Representation of question"""
    __tablename__ = 'questions'

    text = db.Column(db.TEXT, nullable=False)
    quiz_id = db.Column(db.String(60), db.ForeignKey('quizzes.id'), nullable=False)

    answers = db.relationship('Answer', backref='question', lazy=True)

    def __init__(self, text):
        """initializes question"""
        super().__init__()
        self.text = text

 
