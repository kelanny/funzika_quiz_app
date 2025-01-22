#!/usr/bin/env python
"""Contains the tests for the BaseModel class"""

import pytest
from app import create_app, db
from app.user.models import User
import uuid

# Helper function to generate unique email addresses
def unique_email():
    return f"test_user_{uuid.uuid4().hex[:8]}@example.com"

# Test configuration for pytest
@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")  # Ensure the testing config is used
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.rollback()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def test_user():
    """Fixture to provide a clean instance of User for each test."""
    user = User(username="test_user", email=f"test_user@example.com", password_hash="hashed_password")
    return user

def test_user_attributes(test_user):
    """Test that User attributes are initialized correctly."""
    assert test_user.username == "test_user", "Username was not set correctly."
    assert test_user.email == "test_user@example.com", "Email was not set correctly."
    assert test_user.password_hash == "hashed_password", "Password hash was not set correctly."
    assert test_user.is_admin is False, "Default is_admin should be False."

def test_user_to_dict(test_user, test_client):
    """Test the to_dict method of User."""
    test_user.save_to_db()
    user_dict = test_user.to_dict()
    assert isinstance(user_dict, dict), "to_dict should return a dictionary."
    assert user_dict['username'] == "test_user", "to_dict username mismatch."
    assert user_dict['email'] == "test_user@example.com", "to_dict email mismatch."
    assert user_dict['password_hash'] == "hashed_password", "to_dict password_hash mismatch."
    assert user_dict['is_admin'] is False, "to_dict is_admin mismatch."
    test_user.delete_from_db()


def test_user_save_to_db(test_user, test_client):
    """Test saving a User instance to the database."""
    test_user.save_to_db()
    fetched_user = db.session.get(User, test_user.id)  # Corrected query
    assert fetched_user is not None, "User was not saved to the database."
    assert fetched_user.username == test_user.username
    test_user.delete_from_db()


def test_user_delete_from_db(test_user, test_client):
    """Test deleting a User instance from the database."""
    test_user.save_to_db()
    test_user.delete_from_db()
    fetched_user = db.session.get(User, test_user.id)
    assert fetched_user is None, "User was not deleted from the database."


def test_user_is_authenticated(test_user):
    """Test the is_authenticated property."""
    assert test_user.is_authenticated is True, "User should always be authenticated."


def test_user_is_active(test_user):
    """Test the is_active property."""
    assert test_user.is_active is True, "User should always be active."

def test_user_is_anonymous(test_user):
    """Test the is_anonymous property."""
    assert test_user.is_anonymous is False, "User should never be anonymous."


def test_user_get_id(test_user):
    """Test the get_id method."""
    # test_user.save_to_db()
    user_id = test_user.get_id()
    assert user_id == str(test_user.id), "get_id did not return the correct ID."


def test_user_make_admin(test_user, test_client):
    """Test the make_admin method."""
    test_user.save_to_db()
    assert test_user.is_admin is False, "User should not be admin by default."
    test_user.make_admin()
    assert test_user.is_admin is True, "make_admin did not set is_admin to True."
