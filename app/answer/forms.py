from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class SubmitAnswerForm(FlaskForm):
    answer = RadioField('Select an answer', choices=[], coerce=int)
    submit = SubmitField('Submit Answer')
