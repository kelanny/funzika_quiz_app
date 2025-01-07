#!/usr/bin/python3
""" Contains the Question class """
from app.base_model import BaseModel
from app.answer.models import Answer
from app import db


class Question(BaseModel):
    """Representation of question"""
    __tablename__ = 'questions'

    text = db.Column(db.TEXT, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(
        db.String(60),
        db.ForeignKey('quizzes.id'),
        nullable=False
        )

    answers = db.relationship('Answer', backref='question', lazy=True)

    def __init__(self, text, score, quiz_id):
        """initializes question"""
        super().__init__()
        self.text = text
        self.score = score
        self.quiz_id = quiz_id

    def to_dict(self):
        question_dict = super().to_dict()
        question_dict.update({
            'text': self.text,
            'score': self.score,
            'quiz_id': self.quiz_id,
            'answers': self.answers
        })
        return question_dict