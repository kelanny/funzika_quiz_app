#!/usr/bin/python3
""" Contains the Answer class """
from app import db 
from app.models.base_model import BaseModel


class Answer(BaseModel):
    """Representation of answer"""
    __tablename__ = 'answers'
    text = db.Column(db.TEXT, nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.String(60), db.ForeignKey("questions.id"), nullable=False)
    
    
