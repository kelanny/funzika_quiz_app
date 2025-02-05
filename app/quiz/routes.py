"""Routes for the Quiz model."""

from flask_login import login_required, current_user
from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for, session)
from app import db
from app.quiz.models import Quiz
from app.question.models import Question
from app.user.models import User
from app.answer.models import Answer
from app.user_answer.models import UserAnswer
from app.quiz.forms import QuizForm, QuizSelectionForm
from app.question.forms import QuestionNewForm, DeleteQuestionForm, \
                                QuestionForm, AddQuestionForm


quiz_bp = Blueprint('quiz', __name__, template_folder='templates')


@quiz_bp.route('/create', methods=['GET', 'POST'])
def create_quiz():
    """Create a new quiz."""
    form = QuizForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        is_active = form.is_active.data
        quiz = Quiz(
            title=title,
            description=description,
            is_active=is_active
            )
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('quiz.list_quizzes'))
    return render_template(
        'create_quiz.html',
        form=form
    )


@quiz_bp.route('/select', methods=['GET', 'POST'])
@login_required
def select_quiz():
    form = QuizSelectionForm()
    quizzes = Quiz.query.filter_by(is_active=True).all()
    form.quiz.choices = [(quiz.id, quiz.title) for quiz in quizzes]

    if form.validate_on_submit():
        session['quiz_id'] = form.quiz.data
        session['question_index'] = 0  # Start with the first question
        session['score'] = 0  # Initialize score
        session['incorrect_answers'] = []  # Track incorrect answers
        return redirect(url_for('quiz.take_quiz'))
    
    return render_template('select_quiz.html', form=form, quizzes=quizzes)


@quiz_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def take_quiz():
    quiz_id = session.get('quiz_id')
    if not quiz_id:
        flash("Please select a quiz first.", "warning")
        return redirect(url_for('quiz.select_quiz'))

    # Get the current question index
    question_index = session.get('question_index', 0)
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions

    if len(questions) == 0:
        flash("The selected quiz has no questions. Try another quiz.", 'warning')
        return redirect(url_for('quiz.select_quiz'))

    # Check if the quiz is complete
    if question_index >= len(questions):
        return redirect(url_for('quiz.quiz_complete', quiz_id=quiz_id))

    # Get the current question
    current_question = questions[question_index]
    form = QuestionNewForm()
    form.answers.choices = [(answer.id, answer.text) for answer in current_question.answers]

    # Process the submitted answer
    if form.validate_on_submit():
        selected_answer_id = form.answers.data
        selected_answer = Answer.query.get(selected_answer_id)

        user_answer = UserAnswer(
        user_id=current_user.id,  # Assuming you have access to the logged-in user
        question_id=current_question.id,
        selected_answer_id=selected_answer_id
        )
        db.session.add(user_answer)
        db.session.commit()

        # Update score and track incorrect answers
        if selected_answer.is_correct:
            session['score'] += current_question.score
        else:
            session['incorrect_answers'].append({
                'question': current_question.text,
                'correct_answer': next(a.text for a in current_question.answers if a.is_correct),
                'your_answer': selected_answer.text
            })

        # Move to the next question
        session['question_index'] += 1
        return redirect(url_for('quiz.take_quiz'))

    # Render the current question
    return render_template(
        'quiz_question.html',
        form=form,
        question=current_question,
        quiz=quiz,
        question_number=question_index + 1,
        total_questions=len(questions)
    )

# Delete Quiz
@quiz_bp.route('/delete/<string:quiz_id>', methods=['GET', 'POST'])
@login_required
def delete_quiz(quiz_id):
    """Delete a quiz"""
    delete_form = DeleteQuestionForm()
    # Validate CSRF token
    if not delete_form.validate_on_submit():
        flash('Invalid CSRF token. Action denied.', 'danger')
        return redirect(url_for('quiz.list_quizzes'))

    # Proceed with deleting the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()

    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('quiz.list_quizzes'))
    return render_template('delete_quiz.html',
                           delete_form=delete_form, quiz=quiz)


# List Quizzes (for reference)
@quiz_bp.route('/', methods=['GET'])
@login_required
def list_quizzes():
    """List all quizzes"""
    quizzes = Quiz.query.all()
    delete_form = DeleteQuestionForm()  # Create the form instance
    return render_template(
        'list_quizzes.html',
        quizzes=quizzes,
        delete_form=delete_form
        )


@quiz_bp.route('<quiz_id>', methods=['GET', 'POST'])
@login_required
def view_quiz(quiz_id):
    """View a specific quiz and its questions."""
    quiz = Quiz.query.get_or_404(quiz_id)

    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    question_form = QuestionForm()

    if question_form.validate_on_submit():
        new_question = Question(
            text=question_form.text.data,
            quiz_id=quiz.id
        )
        db.session.add(new_question)
        db.session.commit()
        flash('Question created successfully!', 'success')
        return redirect(url_for('quiz.view_quiz', quiz_id=quiz.id))

    return render_template('view_quiz.html',
                           quiz=quiz, question_form=question_form, questions=questions)

@quiz_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Fetch all quizzes
    all_quizzes = Quiz.query.all()

    # Prepare data for the dashboard
    progress_data = []
    for quiz in all_quizzes:
        total_questions = len(quiz.questions)
        user_answers_count = (
            UserAnswer.query.filter_by(user_id=current_user.id).count()
        )
        completion_percentage = (user_answers_count / total_questions) * 100 if total_questions > 0 else 0
        progress_data.append({
            'quiz': quiz,
            'total_questions': total_questions,
            'answered_questions': user_answers_count,
            'completion_percentage': round(completion_percentage, 2)
        })

    return render_template(
        'dashboard.html',
        progress_data=progress_data,
        user=current_user,
    )


# @quiz_bp.route('/<string:quiz_id>/add_question', methods=['POST'])
# @login_required
# def add_question(quiz_id):
#     add_question_form = AddQuestionForm()
#     if add_question_form.validate_on_submit():
#         print("Form validated successfully")
#         print("Quiz ID:", quiz_id)
#         print("Form data:", add_question_form.data)
#         question_text = add_question_form.question_text.data
#         score = int(add_question_form.score.data)
#         answer_1 = add_question_form.answer_1.data
#         answer_2 = add_question_form.answer_2.data
#         answer_3 = add_question_form.answer_3.data
#         answer_4 = add_question_form.answer_4.data
#         correct_answer = int(add_question_form.correct_answer.data)

#         # Create the question
#         question = Question(text=question_text, quiz_id=quiz_id, score=score)
#         db.session.add(question)
#         db.session.commit()

#         # Create the answer answers
#         answers = [
#             Answer(text=answer_1, question_id=question.id, is_correct=(correct_answer == 1)),
#             Answer(text=answer_2, question_id=question.id, is_correct=(correct_answer == 2)),
#             Answer(text=answer_3, question_id=question.id, is_correct=(correct_answer == 3)),
#             Answer(text=answer_4, question_id=question.id, is_correct=(correct_answer == 4)),
#         ]
#         db.session.add_all(answers)
#         db.session.commit()

#         flash('Question and answers added successfully!', 'success')
#         return redirect(url_for('quiz.view_quiz', quiz_id=quiz_id))

#     return render_template('add_question.html', add_question_form=add_question_form, quiz_id=quiz_id)


