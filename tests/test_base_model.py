#!/usr/bin/env python
"""Contains the tests for the BaseModel class"""

import unittest
from app import db, create_app
from app.models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_base_model_creation(self):
        model = BaseModel()
        db.session.add(model)
        db.session.commit()
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)