"""Routes for the application."""
from flask import Blueprint, flash, redirect, render_template, request, url_for 
from app import db
from app.models.quiz import Quiz
from app.models.question import Question
from app.forms.quiz_forms import QuizForm


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
@quiz_blueprint.route('/delete/<string:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('quizzes.list_quizzes'))

# List Quizzes (for reference)
@quiz_blueprint.route('/', methods=['GET'])
def list_quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes/list_quizzes.html', quizzes=quizzes)


@quiz_blueprint.route('<quiz_id>', methods=['GET'])
def view_quiz(quiz_id):
    """View a specific quiz and its questions."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('quizzes/view_quiz.html', quiz=quiz, questions=questions)
