#!/usr/bin/python3
""" Contains the Admin class"""
from app import db 
from app.models.base_model import BaseModel


class Admin(BaseModel):
    """Representation of admin """
    __tablename__ = 'admins'

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(60), nullable=False)

    def __init__(self, role):
        """initializes admin"""
        super().__init__()
        self.role = role

 

