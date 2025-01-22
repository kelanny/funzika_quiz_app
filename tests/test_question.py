#!/usr/bin/env python
"""Contains the tests for the Question class"""


import pytest
from app import create_app, db
from app.question.models import Question
from app.quiz.models import Quiz
import uuid


def setup_quiz():
    quiz = Quiz(id="valid-quiz-id", name="Sample Quiz")
    db.session.add(quiz)
    db.session.commit()
    return quiz

@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.rollback()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def test_question():
    """Fixture to provide a clean instance of Question for each test."""
    quiz = setup_quiz()
    question = Question(text="Sample Question", quiz_id=quiz.id, score=1)
    return question

def test_question_attributes(setup_quiz, test_question):
    """Test that Question attributes are initialized correctly."""
    quiz = setup_quiz
    assert test_question.text == "Sample Question", "Text was not set correctly."
    assert test_question.quiz_id == quiz.id, "quiz_id was not set correctly."
    assert test_question.score == 1, "score should be 1."
    quiz.delete_from_db()


def test_question_to_dict(test_question, test_client):
    """Test the to_dict method of Question."""
    quiz = setup_quiz()
    test_question.save_to_db()
    question_dict = test_question.to_dict()
    assert isinstance(question_dict, dict), "to_dict should return a dictionary."
    assert question_dict['text'] == "Sample Question", "to_dict text mismatch."
    assert question_dict['quiz_id'] == quiz.id, "to_dict quiz_id mismatch."
    assert question_dict['score'] == 1, "to_dict is_active mismatch."
    assert 'answers' in question_dict, "to_dict should include questions."
    test_question.delete_from_db()
    quiz.delete_from_db()

def test_question_save_to_db(test_question, test_client):
    """Test saving a Question instance to the database."""
    test_question.save_to_db()
    fetched_question = db.session.get(Question, test_question.id)
    assert fetched_question is not None, "Question was not saved to the database."
    assert fetched_question.text == test_question.text, "Saved question title mismatch."
    test_question.delete_from_db()


def test_question_delete_from_db(test_question, test_client):
    """Test deleting a Question instance from the database."""
    test_question.save_to_db()
    test_question.delete_from_db()
    fetched_question = db.session.get(Question, test_question.id)
    assert fetched_question is None, "Question was not deleted from the database."
