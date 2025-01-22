""" Contains the Quiz class"""
from app import db
from app.models.base_model import BaseModel
from app.question.models import Question


class Quiz(BaseModel, db.Model):
    """Representation of quiz """
    __tablename__ = 'quizzes'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.TEXT)
    is_active = db.Column(db.Boolean)

    questions = db.relationship('Question', backref='quiz',
                                lazy=True, cascade='all, delete, delete-orphan')

    def __init__(self, title, description, is_active=False):
        """Instantiates a new quiz"""
        super().__init__()
        self.title = title
        self.description = description
        self.is_active = is_active

    def to_dict(self):
        quiz_dict = super().to_dict()
        quiz_dict.update({
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'questions': self.questions
        })
        return quiz_dict
