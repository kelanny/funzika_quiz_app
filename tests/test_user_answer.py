#!/usr/bin/env python
"""Contains the tests for the UserAnswer class"""

import unittest
from datetime import datetime
from app import db, create_app
from app.models.user_answer import UserAnswer
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.models.quiz import Quiz


class TestUserAnswerModel(unittest.TestCase):
    """Tests for the UserAnswer class"""

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
    
    def test_user_answer_creation(self):
        """Test the creation of a user_answer"""

        user = User(username='testuser', email="testuser@gmail.com")
        db.session.add(user)
        db.session.commit()
        quiz = Quiz(title='Sample Quiz', description='This is a sample quiz', is_active=True)
        db.session.add(quiz)
        db.session.commit()
        question = Question(quiz_id=quiz.id, question='What is the capital of Kenya?')
        db.session.add(question)
        db.session.commit()
        answer = Answer(question_id=question.id, answer='Nairobi', is_correct=True)
        db.session.add(answer)
        db.session.commit()
        user_answer = UserAnswer(user_id=user.id, answer_id=answer.id)
        db.session.add(user_answer)
        db.session.commit()
        self.assertEqual(user_answer.user_id, user.id)
        self.assertEqual(user_answer.answer_id, answer.id)
        self.assertIsNotNone(user_answer.id)
        self.assertIsInstance(user_answer.created_at, datetime)
        self.assertIsInstance(user_answer.updated_at, datetime)
