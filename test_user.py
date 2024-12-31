#!/usr/bin/env python
"""Test user models"""

from app.models.user import User
from app import db, create_app


def test_create_user():
    """Test create user"""
    user1 = User(username='test_user', email="user1@gmail.com", password='user1')
    db.session.add(user1)
    user2 = User(username='test_user2', email="user2@gmail.com", password='user2')
    db.session.add(user2)
    user3 = User(username='test_user3', email="user3@gmail.com", password='user3')
    db.session.add(user3)
    db.session.commit()



def test_get_users():
    """Test get users"""
    users = User.query.all()
    
    for user in users:
        print(f"\nUsername: {user.username}\nEmail: {user.email}\n{('=' * 50)}")


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
        # test_create_user()
        test_get_users()