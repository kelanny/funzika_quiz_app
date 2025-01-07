#!/usr/bin/python3
""" Contains the Answer class """
from app import db
from app.base_model import BaseModel


class Answer(BaseModel):
    """Representation of answer"""
    __tablename__ = 'answers'
    text = db.Column(db.TEXT, nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.String(60),
                            db.ForeignKey("questions.id"), nullable=False)

    def __init__(self, text, question_id, is_correct=False):
        """Initialize the answer"""
        super().__init__()
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id

    def to_dict(self):
        answer_dict = super().to_dict()
        answer_dict.update({
            'text': self.text,
            'is_correct': self.is_correct,
            'question_id': self.question_id
        })
