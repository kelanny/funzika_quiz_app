#!/usr/bin/env python
"""Contains the tests for the Answer class"""

import unittest
from app import db, create_app
from app.models.question import Question
from app.models.answer import Answer

class TestAnswerModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_answer_foreign_key(self):
        # Create a parent Question object
        question = Question(text="What is the capital of France?")
        db.session.add(question)
        db.session.commit()

        # Create a child Answer object linked to the Question
        answer = Answer(text="Paris", is_correct=True, question_id=question.id)
        db.session.add(answer)
        db.session.commit()

        # Assert that the foreign key is correctly set
        self.assertEqual(answer.question_id, question.id)

        # Assert that the relationship resolves correctly
        self.assertEqual(answer.question, question)
