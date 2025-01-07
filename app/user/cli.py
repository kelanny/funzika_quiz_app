#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.user.models import User
from app.question.models import Question
from app.answer.models import Answer


# User CLI group
user_cli = AppGroup("user")


@user_cli.command("add")
@click.option("--username", prompt=True, help="The username of the user.")
@click.option(("--email"), prompt=True, help="The email of the user.")
@click.option("--password", prompt=True, hide_input=True,
              confirmation_prompt=True, help="The password of the user.")
@click.option("--is_admin", prompt=True,
              type=bool, help="Whether the user is an admin.")
def add_user(username, email, password, is_admin):
    """Add a new user."""
    from app import bcrypt

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email,
                password_hash=hashed_password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User '{username}' added successfully.")


@user_cli.command("add-admin")
@click.option("--username", prompt=True, help="The username of the user.")
@click.option(("--email"), prompt=True, help="The email of the user.")
@click.option("--password", prompt=True, hide_input=True,
              confirmation_prompt=True, help="The password of the user.")
@click.option("--is_admin", prompt=True, type=bool,
              default=True, help="Whether the user is an admin.")
def add_admin(username, email, password, is_admin):
    """Add a new user."""
    from app import bcrypt

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email,
                password_hash=hashed_password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User '{username}' added successfully.")


@user_cli.command("list")
def list_users():
    """List all users."""
    users = User.query.all()
    if not users:
        click.echo("No users found.")
        return
    click.echo("List of users:")
    click.echo("Number of users: {}".format(len(users)))
    click.echo("-" * 100)

    for idx, user in enumerate(users, 1):
        click.echo("#: {}".format(idx))
        click.echo(
            f"User ID:{user.id}"
            f"\nUsername: {user.username}"
            f"\nEmail: {user.email}"
            f"\nRole: {'Admin' if user.is_admin else 'User'}\n"
        )
        click.echo("-" * 100)


@user_cli.command("delete")
@click.option('--user_id', default=None, type=int, help='User ID')
@click.option('--username', default=None, type=str, help='Username')
@click.option('--email', default=None, type=str, help="User email")
def delete_user(user_id=None, username=None, email=None):
    """Delete selected user from the database."""
    user = None
    # Fetch user based on the provided argument
    if user_id:
        user = User.query.get(user_id)  # Get by primary key
    elif username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        click.echo("You must provide either --user_id, --username, or --email.")
        return

    # Handle case where user is not found
    if not user:
        click.echo("User not found.")
        return

    db.session.delete(user)
    db.session.commit()
    click.echo(f"User '{user.username}' deleted successfully.")


@user_cli.command("view")
@click.option('--user_id', default=None, type=int, help='User ID')
@click.option('--username', default=None, type=str, help='Username')
@click.option('--email', default=None, type=str, help="User email")
def view_user(user_id=None, username=None, email=None):
    """View user details."""
    user = None
    # Fetch user based on the provided argument
    if user_id:
        user = User.query.get(user_id)  # Get by primary key
    elif username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        click.echo("You must provide either --user_id, --username, or --email.")
        return

    # Handle case where user is not found
    if not user:
        click.echo("User not found.")
        return

    click.echo(
        f"User ID:{user.id}"
        f"\nUsername: {user.username}"
        f"\nEmail: {user.email}"
        f"\nRole: {'Admin' if user.is_admin else 'User'}\n"
        )


@user_cli.command('list_answers')
@click.option('--user_id', default=None, type=int, help='User ID')
@click.option('--username', default=None, type=str, help='Username')
@click.option('--email', default=None, type=str, help="User email")
def list_user_answers(user_id=None, username=None, email=None):
    """List all answers selected by this user."""
    user = None

    # Fetch user based on the provided argument
    if user_id:
        user = User.query.get(user_id)  # Get by primary key
    elif username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        click.echo("You must provide either --user_id, --username, or --email.")
        return

    # Handle case where user is not found
    if not user:
        click.echo("User not found.")
        return

    # List user's selected answers
    selected_answers = user.user_answers  # Assuming `user_answers` is a relationship on the `User` model
    total_score = 0

    click.echo(f"Username: {user.username}")
    click.echo(f"User ID: {user.id}")
    click.echo(f"Attempted questions: {len(selected_answers)}")
    click.echo("Selected Answers:\n")

    for idx, answer in enumerate(selected_answers, 1):
        question = Question.query.get(answer.question_id)
        selected_answer = Answer.query.get(answer.selected_answer_id)

        if selected_answer.is_correct:
            status = 'Correct'
            score = question.score
        else:
            status = 'Wrong'
            score = 0
        total_score += score

        click.echo(
            f"\t#: {idx}\n"
            f"\tQuestion: {question.text}\n"
            f"\tAnswer: {selected_answer.text}\n"
            f"\tStatus: {status}\n"
            f"\tScore: {score}\n"
        )

    click.echo("\nTotal Score: {}".format(total_score))
    click.echo("-" * 100)
