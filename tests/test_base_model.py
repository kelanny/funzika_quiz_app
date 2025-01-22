#!/usr/bin/env python
"""Contains the tests for the BaseModel class"""

import pytest
from datetime import datetime
from app import create_app, db
from app.models.base_model import BaseModel
import uuid

# A concrete model inheriting from BaseModel for testing purposes
class MyTestModel(BaseModel):
    __tablename__ = 'test_model'
    name = db.Column(db.String(100), nullable=False)

# Test configuration for pytest
@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")  # Ensure you have a 'testing' config in your app
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def test_instance():
    """Fixture to provide a clean instance of MyTestModel for each test."""
    instance = MyTestModel(name="Test Name")
    return instance

def test_basemodel_attributes(test_instance, test_client):
    """Test that BaseModel attributes are initialized correctly."""
    test_instance.save_to_db()
    assert isinstance(test_instance.id, str), "ID should be a string."
    assert len(test_instance.id) > 0, "ID should not be empty."
    assert isinstance(test_instance.created_at, datetime), "created_at should be a datetime object."
    assert isinstance(test_instance.updated_at, datetime), "updated_at should be a datetime object."

def test_basemodel_str(test_instance):
    """Test the __str__ method of BaseModel."""
    expected_str = f"<MyTestModel {test_instance.id}>"
    assert str(test_instance) == expected_str, "String representation is incorrect."

def test_basemodel_save_to_db(test_instance, test_client):
    """Test saving an instance to the database."""
    test_instance.save_to_db()
    fetched_instance = db.session.get(MyTestModel, test_instance.id)
    assert fetched_instance is not None, "Instance was not saved to the database."
    assert fetched_instance.name == test_instance.name, "Saved instance data is incorrect."

def test_basemodel_delete_from_db(test_instance, test_client):
    """Test deleting an instance from the database."""
    test_instance.save_to_db()
    test_instance.delete_from_db()
    fetched_instance = db.session.get(MyTestModel, test_instance.id)
    assert fetched_instance is None, "Instance was not deleted from the database."

def test_basemodel_to_dict(test_instance):
    """Test the to_dict method of BaseModel."""
    test_instance_dict = test_instance.to_dict()
    assert isinstance(test_instance_dict, dict), "to_dict should return a dictionary."
    assert "id" in test_instance_dict, "to_dict should include the 'id' field."
    assert "created_at" in test_instance_dict, "to_dict should include the 'created_at' field."
    assert "updated_at" in test_instance_dict, "to_dict should include the 'updated_at' field."
    assert test_instance_dict["name"] == test_instance.name, "to_dict should include instance-specific fields."
