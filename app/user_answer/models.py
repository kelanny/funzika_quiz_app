#!/usr/bin/python3
""" Contains the UserAnswer class"""
from app import db
from app.base_model import BaseModel


class UserAnswer(BaseModel):
    """Representation of user_answer """
    __tablename__ = 'user_answers'

    user_id = db.Column(db.String(60),
                        db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.String(60),
                            db.ForeignKey("questions.id"), nullable=False)
    selected_answer_id = db.Column(db.String(36),
                                   db.ForeignKey('answers.id'), nullable=False)

    def __init__(self, user_id, question_id, selected_answer_id):
        """Initializes the UserAnswer instances"""
        super().__init__()
        self.user_id = user_id
        self.question_id = question_id
        self.selected_answer_id = selected_answer_id

    def to_dict(self):
        user_answer_dict = super().to_dict()
        user_answer_dict.update({
            'user_id': self.user_id,
            'question_id': self.question_id,
            'selected_answer_id': self.selected_answer_id
        })
