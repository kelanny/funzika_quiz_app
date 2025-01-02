#!/usr/bin/env python
""" Contains the Question routes """

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required
from app.models.question import Question
from app.models.quiz import Quiz
from app.forms.question_forms import QuestionForm, DeleteQuestionForm

questions_bp = Blueprint('questions', __name__, template_folder='templates')

@questions_bp.route('/')
def list_questions():
    """List all questions"""
    questions = Question.query.all()
    delete_form = DeleteQuestionForm()  # Create the form instance
    return render_template(
        'questions/list.html',
        questions=questions,
        delete_form=delete_form
        )

@questions_bp.route('/new', methods=['GET', 'POST'])
def create_question():
    """Create a new question"""
    form = QuestionForm()
    form.quiz_id.choices = [(quiz.id, quiz.title) for quiz in Quiz.query.all()]
    
    if form.validate_on_submit():
        question = Question(text=form.text.data, quiz_id=form.quiz_id.data)
        db.session.add(question)
        db.session.commit()
        flash('Question created successfully!', 'success')
        return redirect(url_for('questions.list_questions'))

    return render_template('questions/new.html', form=form)

@questions_bp.route('/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    """Edit an existing question"""
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    form.quiz_id.choices = [(quiz.id, quiz.title) for quiz in Quiz.query.all()]
    
    if form.validate_on_submit():
        question.text = form.text.data
        question.quiz_id = form.quiz_id.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('questions.list_questions'))
    
    return render_template('questions/edit.html', form=form, question=question)

# @questions_bp.route('/<question_id>')
# def view_question(question_id):
#     """Display a single question's details."""
#     question = Question.query.get_or_404(question_id)
#     return render_template('questions/view_question.html', question=question)

@questions_bp.route('/<question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    """Confirm and delete a question"""
    question = Question.query.get_or_404(question_id)
    delete_form = DeleteQuestionForm()

    if request.method == 'POST' and delete_form.validate_on_submit():
        db.session.delete(question)
        db.session.commit()
        flash('Question deleted successfully!', 'success')
        return redirect(url_for('questions.list_questions'))

    return render_template('questions/delete.html', question=question, delete_form=delete_form)
