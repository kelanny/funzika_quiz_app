#!/usr/bin/python3
""" Contains the UserAnswer class"""
from app import db 
from app.models.base_model import BaseModel


class UserAnswer(BaseModel):
    """Representation of user_answer """
    __tablename__ = 'user_answers'

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.String(60), db.ForeignKey("questions.id"), nullable=False)
    selected_answer = db.Column(db.String(36), db.ForeignKey('answers.id'), nullable=False)
 

