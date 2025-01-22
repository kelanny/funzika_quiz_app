#!/usr/bin/env python
"""Contains the tests for the Quiz class"""

import pytest
from app import create_app, db
from app.quiz.models import Quiz


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
def test_quiz():
    """Fixture to provide a clean instance of Quiz for each test."""
    quiz = Quiz(title="Sample Quiz", description="This is a sample quiz description.", is_active=True)
    return quiz

def test_quiz_attributes(test_quiz):
    """Test that Quiz attributes are initialized correctly."""
    assert test_quiz.title == "Sample Quiz", "Title was not set correctly."
    assert test_quiz.description == "This is a sample quiz description.", "Description was not set correctly."
    assert test_quiz.is_active is True, "is_active should be True."

def test_quiz_to_dict(test_quiz, test_client):
    """Test the to_dict method of Quiz."""
    test_quiz.save_to_db()
    quiz_dict = test_quiz.to_dict()
    assert isinstance(quiz_dict, dict), "to_dict should return a dictionary."
    assert quiz_dict['title'] == "Sample Quiz", "to_dict title mismatch."
    assert quiz_dict['description'] == "This is a sample quiz description.", "to_dict description mismatch."
    assert quiz_dict['is_active'] is True, "to_dict is_active mismatch."
    assert 'questions' in quiz_dict, "to_dict should include questions."
    test_quiz.delete_from_db()

def test_quiz_save_to_db(test_quiz, test_client):
    """Test saving a Quiz instance to the database."""
    test_quiz.save_to_db()
    fetched_quiz = db.session.get(Quiz, test_quiz.id)
    assert fetched_quiz is not None, "Quiz was not saved to the database."
    assert fetched_quiz.title == test_quiz.title, "Saved quiz title mismatch."
    test_quiz.delete_from_db()

def test_quiz_delete_from_db(test_quiz, test_client):
    """Test deleting a Quiz instance from the database."""
    test_quiz.save_to_db()
    test_quiz.delete_from_db()
    fetched_quiz = db.session.get(Quiz, test_quiz.id)
    assert fetched_quiz is None, "Quiz was not deleted from the database."
