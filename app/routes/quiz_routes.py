"""Routes for the application."""
from flask import Blueprint, flash, redirect, render_template, request, url_for 
from app import db
from app.models.quiz import Quiz


quiz_blueprint = Blueprint('quizzes', __name__, template_folder='templates')


@quiz_blueprint.route('/create/', methods=['GET', 'POST'])
def create():
    """Create a new quiz."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        is_active = request.form.get('is_active') == 'on'

        #Validate the data
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('quizzes.create_quiz'))
        
        # Create the quiz
        quiz = Quiz(title=title, description=description, is_active=is_active)
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully.', 'success')
        return redirect(url_for('quizzes.list_quizzes'))

    return render_template('quizzes/create_quiz.html')

@quiz_blueprint.route('/')
def list_quizzes():
    """List all quizzes."""
    quizzes = Quiz.query.filter_by(is_active=True).all()
    return render_template('quizzes/list_quizzes.html', quizzes=quizzes)

@quiz_blueprint.route('/<quiz_id>/')
def view_quiz(quiz_id):
    """View a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quizzes/view_quiz.html', quiz=quiz)

@quiz_blueprint.route('/edit/<string:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        quiz.title = request.form['title']
        quiz.description = request.form['description']
        quiz.is_active = True if request.form.get('is_active') == 'on' else False

        try:
            db.session.commit()
            flash('Quiz updated successfully!', 'success')
            return redirect(url_for('quizzes.list_quizzes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating quiz: {str(e)}', 'danger')

    return render_template('quizzes/edit_quiz.html', quiz=quiz)

@quiz_blueprint.route('/delete/<string:quiz_id>', methods=['GET', 'POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        try:
            db.session.delete(quiz)
            db.session.commit()
            flash('Quiz deleted successfully!', 'success')
            return redirect(url_for('quizzes.list_quizzes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting quiz: {str(e)}', 'danger')

    return render_template('quizzes/delete_quiz.html', quiz=quiz)
