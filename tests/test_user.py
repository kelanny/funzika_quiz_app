#!/usr/bin/env python
"""Contains the tests for the User class"""

import unittest
from app import db, create_app
from app.models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')

        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertIsNotNone(user.id)