#!/usr/bin/env python
"""Quiz Forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class QuizForm(FlaskForm):
    """Quiz form class"""
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Save')


class DeleteQuizForm(FlaskForm):
    """Quiz delete form class"""
    submit = SubmitField('Delete')
