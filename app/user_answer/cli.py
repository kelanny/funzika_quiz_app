#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.answer.models import Answer
from app.user_answer.models import UserAnswer
from app.question.models import Question
from app.user.models import User


# User CLI group
user_answer_cli = AppGroup("user_answer")


@user_answer_cli.command("add")
@click.option('--user_id', default=None, type=str, help="Id of the associated user")
@click.option('--username', default=None, type=str, help='Username')
@click.option('--email', default=None, type=str, help="User email")
@click.option('--question_id', help="The id of  associated question")
@click.option('--selected_answer_id', help="Id of the selected answer")
def add_user_answers(question_id, selected_answer_id, user_id=None, username=None, email=None):
    """Add data to the user_answers table in the database"""
    user = None

    # Fetch user based on the provided argument
    if user_id:
        user = User.query.get(user_id)  # Get by primary key
    elif username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()

    # Handle case where user is not found
    if not user:
        click.echo(f"User belonging to this ID: ({user_id}) was not found.")

    question = Question.query.get(question_id)
    if not question:
        click.echo(f"No question belonging to this ID: ({question_id}) was found.")
    selected_answer = Answer.query.get(selected_answer_id)
    if not selected_answer:
        click.echo(f"The answer selected by the user was not found.")

    user_answer = UserAnswer(
        user_id=user.id,
        question_id=question_id,
        selected_answer_id=selected_answer_id
    )
    db.session.add(user_answer)
    db.session.commit()
    click.echo('User answer added successfully.')


@user_answer_cli.command("list")
@click.argument('username')
def list_user_answers(username):
    """List all answers selected by user"""
    user = User.query.get(username)

    user_answers = UserAnswer.query.get(user.id).all()
    if not user_answers:
        print("No answers associated to this user found.")