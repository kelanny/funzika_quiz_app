#!/usr/bin/env python
"""Contains the tests for the Question class"""

# tests/test_question.py
from flask_sqlalchemy import db, create_app
import unittest
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.answer import Answer

class TestQuestionModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_question_foreign_key(self):
        # Create a parent Quiz object
        self.quiz = Quiz(title="Sample Quiz", description="A sample quiz")
        db.session.add(self.quiz)
        db.session.commit()

        # Create a child Question object linked to the Quiz
        self.question = Question(text="What is the capital of France?", quiz_id=self.quiz.id)
        db.session.add(self.question)
        db.session.commit()

        # Assert that the foreign key is correctly set
        self.assertEqual(self.question.quiz_id, self.quiz.id)
        self.assertEqual(self.question.text, "What is the capital of France?")

        # Assert that the relationship resolves correctly
        self.assertEqual(self.question.quiz, self.quiz)
