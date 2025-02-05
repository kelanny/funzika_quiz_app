#!/usr/bin/env python
"""Question form module"""

from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, BooleanField,
                     FieldList, FormField, SubmitField,
                     IntegerField, SelectField, RadioField)
from wtforms.validators import DataRequired, Length


class AnswerForm(FlaskForm):
    text = StringField('Answer', validators=[DataRequired(), Length(max=255)])
    is_correct = BooleanField('Correct Answer')


class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question Text', validators=[DataRequired(), Length(max=1000)])
    # quiz_id = SelectField('Quiz', validators=[DataRequired()])
    score = IntegerField('Question Score', validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=4, max_entries=4)
    submit = SubmitField('Add Question')


# class QuestionForm(FlaskForm):
#     """Question form class"""

#     quiz_id = SelectField('Quiz', validators=[DataRequired()])
#     text = TextAreaField('Question Text', validators=[DataRequired()])
#     submit = SubmitField('Submit')

class DeleteQuestionForm(FlaskForm):
    """Delete question form class"""
    submit = SubmitField('Delete')

class QuestionNewForm(FlaskForm):
    answers = RadioField("Select an Answer", validators=[DataRequired()])
    submit = SubmitField("Submit Answer")


class AddQuestionForm(FlaskForm):
    quiz_id = SelectField('Quiz', validators=[DataRequired()])
    text = StringField('Question Text', validators=[DataRequired()])
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
