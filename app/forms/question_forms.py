#!/usr/bin/env python
"""Question form module"""


# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models.quiz import Quiz


class QuestionForm(FlaskForm):
    text = TextAreaField('Question Text', validators=[DataRequired()])
    quiz_id = SelectField('Quiz', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate quiz choices dynamically
        self.quiz_id.choices = [(quiz.id, quiz.title)
                                for quiz in Quiz.query.all()]
