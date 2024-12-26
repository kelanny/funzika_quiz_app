#!/usr/bin/env python
"""Contains the tests for the Admin class"""

import unittest
from datetime import datetime
from app import db, create_app
from app.models.admin import Admin
from app.models.user import User


class TestAdminModel(unittest.TestCase):
    """Tests for the Admin class"""

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
    
    def test_admin_creation(self):
        """Test the creation of an admin"""

        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        admin = Admin(user_id=user.id, role='admin')
        db.session.add(admin)
        db.session.commit()
        self.assertEqual(admin.user_id, user.id)
        self.assertEqual(admin.role, 'admin')
        self.assertIsNotNone(admin.id)
        self.assertIsInstance(admin.created_at, datetime)
        self.assertIsInstance(admin.updated_at, datetime)


