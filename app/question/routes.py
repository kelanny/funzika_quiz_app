#!/usr/bin/env python
""" Contains the Question routes """

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required
from app.question.models import Question
from app.quiz.models import Quiz
from app.answer.models import Answer
from app.question.forms import QuestionForm, DeleteQuestionForm


questions_bp = Blueprint('questions', __name__, template_folder='templates')


@questions_bp.route('/')
def list_questions():
    """List all questions"""
    questions = Question.query.all()
    delete_form = DeleteQuestionForm()  # Create the form instance
    return render_template(
        'list_questions.html',
        questions=questions,
        delete_form=delete_form
        )


# @questions_bp.route('/new', methods=['GET', 'POST'])
# def create_question():
#     """Create a new question"""
#     form = AddQuestionForm()
#     form.quiz_id.choices = [(quiz.id, quiz.title) for quiz in Quiz.query.all()]

#     if form.validate_on_submit():
#         text = form.text.data
#         quiz_id = form.quiz_id.data
#         score = form.score.data
#         answer_1 = form.answer_1.data
#         answer_2 = form.answer_2.data
#         answer_3 = form.answer_3.data
#         answer_4 = form.answer_4.data
#         correct_answer = int(form.correct_answer.data)

#         question = Question(text=text, quiz_id=quiz_id, score=score)
#         db.session.add(question)
#         db.session.commit()
#         flash('Question created successfully!', 'success')
#         return redirect(url_for('questions.list_questions'))

#     return render_template('add_question.html', form=form)


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

    return render_template('edit.html', form=form, question=question)


@questions_bp.route('/<question_id>')
def view_question(question_id):
    """Display a single question's details."""
    question = Question.query.get_or_404(question_id)
    return render_template('view_question.html', question=question)


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

    return render_template('delete.html',
                           question=question, delete_form=delete_form)


@questions_bp.route('/add_question/<quiz_id>', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()

    if form.validate_on_submit():
        # Extract question text
        question_text = form.question_text.data
        score = int(form.score.data)
        # Validate that at least one correct answer is selected
        if not any(answer.is_correct.data for answer in form.answers):
            flash("At least one answer must be marked as correct.", "danger")
            return render_template('admin_add_question.html', quiz=quiz, form=form)

        # Add the question to the database
        question = Question(quiz_id=quiz.id, text=question_text, score=score)
        db.session.add(question)
        db.session.flush()  # Flush to get the question.id

        # Add answers
        for answer_form in form.answers:
            answer = Answer(
                question_id=question.id,
                text=answer_form.text.data,
                is_correct=answer_form.is_correct.data
            )
            db.session.add(answer)

        db.session.commit()
        flash("Question and answers added successfully!", "success")
        return redirect(url_for('questions.list_questions'))  # Replace with your admin dashboard route

    return render_template('admin_add_question.html', quiz=quiz, form=form)