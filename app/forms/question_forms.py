#!/usr/bin/env python
"""Question form module"""


# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models.quiz import Quiz

class QuestionForm(FlaskForm):
    """Question form class"""

    quiz_id = SelectField('Quiz', validators=[DataRequired()])
    text = TextAreaField('Question Text', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteQuestionForm(FlaskForm):
    """Delete question form class"""
    submit = SubmitField('Delete')
