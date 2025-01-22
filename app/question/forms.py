#!/usr/bin/env python
"""Question form module"""


# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    """Question form class"""

    quiz_id = SelectField('Quiz', validators=[DataRequired()])
    text = TextAreaField('Question Text', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteQuestionForm(FlaskForm):
    """Delete question form class"""
    submit = SubmitField('Delete')

class QuestionNewForm(FlaskForm):
    answers = RadioField("Select an Answer", validators=[DataRequired()])
    submit = SubmitField("Submit Answer")


class AddQuestionForm(FlaskForm):
    question_text = StringField('Question Text', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    answer_1 = StringField('Answer 1', validators=[DataRequired()])
    answer_2 = StringField('Answer 2', validators=[DataRequired()])
    answer_3 = StringField('Answer 3', validators=[DataRequired()])
    answer_4 = StringField('Answer 4', validators=[DataRequired()])
    correct_answer = SelectField(
        'Correct Answer',
        choices=[('1', 'Answer 1'), ('2', 'Answer 2'), ('3', 'Answer 3'), ('4', 'Answer 4')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Question')
