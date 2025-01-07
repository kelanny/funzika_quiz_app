"""Routes for the application."""

from flask_login import login_required
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from app import db
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.answer import Answer
from app.forms.quiz_forms import QuizForm
from app.forms.question_forms import QuestionForm, DeleteQuestionForm


quiz_blueprint = Blueprint('quizzes', __name__, template_folder='templates')

@quiz_blueprint.route('/create', methods=['GET', 'POST'])
def create_quiz():
    """Create a new quiz."""
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('quizzes.list_quizzes'))
    return render_template('quizzes/create_quiz.html', form=form)

# Edit Quiz
@quiz_blueprint.route('/edit/<string:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.is_active = form.is_active.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('quizzes.list_quizzes'))
    return render_template('quizzes/edit_quiz.html', form=form, quiz=quiz)

# Delete Quiz
@quiz_blueprint.route('/<string:quiz_id>/delete', methods=['POST'])
def delete_quiz(quiz_id):
    """Delete a quiz"""
    delete_form = DeleteQuestionForm()
    # Validate CSRF token
    if not delete_form.validate_on_submit():
        flash('Invalid CSRF token. Action denied.', 'danger')
        return redirect(url_for('quizzes.list_quizzes'))

    # Proceed with deleting the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()

    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('quizzes.list_quizzes'))
    return render_template('quizzes/delete_quiz.html', delete_form=delete_form, quiz=quiz)

# List Quizzes (for reference)
@quiz_blueprint.route('/', methods=['GET'])
def list_quizzes():
    """List all quizzes"""
    quizzes = Quiz.query.all()
    delete_form = DeleteQuestionForm()  # Create the form instance
    return render_template(
        'quizzes/list_quizzes.html',
        quizzes=quizzes,
        delete_form=delete_form
        )


@quiz_blueprint.route('<quiz_id>', methods=['GET', 'POST'])
@login_required
def view_quiz(quiz_id):
    """View a specific quiz and its questions."""
    quiz = Quiz.query.get_or_404(quiz_id)

    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('quizzes/view_quiz.html', quiz=quiz, questions=questions)

    question_form = QuestionForm()

    if question_form.validate_on_submit():
        new_question = Question(
            text=question_form.text.data,
            quiz_id=quiz.id
        )
        db.session.add(new_question)
        db.session.commit()
        flash('Question created successfully!', 'success')
        return redirect(url_for('quizzes.view_quiz', quiz_id=quiz.id))

    return render_template('quizzes/view_quiz.html', quiz=quiz, question_form=question_form)

@quiz_blueprint.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    """Display quiz questions and handle user answers."""
    # Fetch current question index from session
    current_question_index = session.get('current_question_index', 0)

    # Get the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Get all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Check if there are no more questions
    if current_question_index >= len(questions):
        # Redirect to the results page or completion page
        return redirect(url_for('quizzes.list_quizzes', quiz_id=quiz_id))
    
    # Get the current question and its answers
    current_question = questions[current_question_index]
    answers = Answer.query.filter_by(question_id=current_question.id).all()
    
    if request.method == 'POST':
        # Handle user answer submission
        selected_answer_id = request.form.get('answer')
        selected_answer = Answer.query.get(selected_answer_id)
        
        # Update score if the answer is correct
        if selected_answer and selected_answer.is_correct:
            session['score'] = session.get('score', 0) + 1
        
        # Move to the next question
        session['current_question_index'] += 1
        
        # Redirect to reload the page
        return redirect(url_for('quiz', quiz_id=quiz_id))
    
    # Render the template with the current question and answers
    return render_template(
        'quiz.html',
        quiz=quiz,
        question=current_question,
        answers=answers,
        progress=current_question_index + 1,
        total=len(questions),
        score=session.get('score', 0)
    )

