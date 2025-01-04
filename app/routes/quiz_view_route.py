from flask import render_template, request, session, redirect, url_for
import app
from app.models.question import Question
from app.models.answer import Answer


@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    """Display quiz questions and handle user answers."""
    # Fetch current question index from session
    current_question_index = session.get('current_question_index', 0)
    
    # Get all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Check if there are no more questions
    if current_question_index >= len(questions):
        # Redirect to the results page or completion page
        return redirect(url_for('quiz_complete', quiz_id=quiz_id))
    
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
        question=current_question,
        answers=answers,
        progress=current_question_index + 1,
        total=len(questions),
        score=session.get('score', 0)
    )
