#!/usr/bin/env python
"""Contains the tests for the Quiz class"""

import unittest
from app import db, create_app
from app.models.quiz import Quiz

class TestQuizModel(unittest.TestCase):
    """Tests for the Quiz class"""

    def setUp(self):
        """Set up the test environment"""

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the test environment"""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_quiz_creation(self):
        """Test the creation of a quiz"""

        quiz = Quiz(title='Sample Quiz', description='This is a sample quiz', is_active=True)
        db.session.add(quiz)
        db.session.commit()
        self.assertEqual(quiz.title, 'Sample Quiz')
        self.assertEqual(quiz.description, 'This is a sample quiz')
        self.assertTrue(quiz.is_active)
        self.assertIsNotNone(quiz.id)