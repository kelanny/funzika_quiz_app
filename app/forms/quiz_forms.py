#!/usr/bin/env python
"""Quiz Forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Save')
