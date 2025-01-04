#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.models.user import User
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.answer import Answer

# Quiz CLI group
quiz_cli = AppGroup("quiz")


@quiz_cli.command("add")
@click.argument("title")
@click.argument("description")
@click.argument("is_active", type=bool, default=True)
def add_quiz(title, description, is_active):
    """Add a new quiz."""
    quiz = Quiz(title=title, description=description, is_active=is_active)
    db.session.add(quiz)
    db.session.commit()
    click.echo(f"Quiz '{title}' added successfully.")


@quiz_cli.command("list")
def list_quizzes():
    """List all quizzes."""
    quizzes = Quiz.query.all()
    if not quizzes:
        click.echo("No quizzes found.")
        return

    for quiz in quizzes:
        click.echo(f"{quiz.id}: {quiz.title} - {quiz.description} - Active: {quiz.is_active}")


@quiz_cli.command("delete")
@click.argument("quiz_id")
def delete_quiz(quiz_id):
    """Delete a quiz."""
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        click.echo(f"Quiz '{quiz.title}' deleted successfully.")
    else:
        click.echo(f"Quiz with ID {quiz_id} not found.")

@quiz_cli.command("view")
@click.argument("quiz_id")
def view_quiz(quiz_id):
    """View a quiz."""
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        click.echo(f"Quiz ID: {quiz.id}")
        click.echo(f"Title: {quiz.title}")
        click.echo(f"Description: {quiz.description}")
        click.echo(f"Active: {quiz.is_active}")
        click.echo('-' * 100)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            click.echo("No questions found for this quiz.")
            return
        else:
            for idx, question in enumerate(questions, 1):
                answers = Answer.query.filter_by(question_id=question.id).all()
                click.echo(f"Question ({idx}): {question.text}")
                click.echo("Answers:")
                for answer in answers:
                    click.echo(f"\t- {answer.text} - Correct: {answer.is_correct}")
                click.echo("-" * 100)
                click.echo()
        
    else:
        click.echo(f"Quiz with ID {quiz_id} not found.")


# Question CLI group
question_cli = AppGroup("question")


@question_cli.command("add")
@click.argument("text")
@click.argument("quiz_id")
def add_question(text, quiz_id):
    """Add a new question."""
    question = Question(text=text, quiz_id=quiz_id)
    db.session.add(question)
    db.session.commit()
    click.echo(f"Question '{text}' added successfully.")


@question_cli.command("list")
def list_questions():
    """List all questions."""
    questions = Question.query.all()
    if not questions:
        click.echo("No questions found.")
        return
    
    for idx, question in enumerate(questions, 1):
        click.echo(f"{idx}: {question.id}: {question.text}")
        answers = question.answers
        click.echo("Answers:")
        for answer in answers:
            click.echo(f"\t- {answer.text} - Correct: {answer.is_correct}")
        click.echo("-" * 100)
        click.echo()

@question_cli.command("delete")
@click.argument("question_id")
def delete_question(question_id):
    """Delete a question."""
    question = Question.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
        click.echo(f"Question '{question.text}' deleted successfully.")
    else:
        click.echo(f"Question with ID {question_id} not found.")


# Answer CLI group
answer_cli = AppGroup("answer")


@answer_cli.command("add")
@click.argument("text")
@click.argument("is_correct", type=bool)
@click.argument("question_id")
def add_answer(text, is_correct, question_id):
    """Add a new answer."""
    answer = Answer(text=text, is_correct=is_correct, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    click.echo(f"Answer '{text}' added successfully.")


@answer_cli.command("list")
def list_answers():
    """List all answers."""
    answers = Answer.query.all()
    if not answers:
        click.echo("No answers found.")
        return
    click.echo(f"Question: {Question.query.get(answers[0].question_id).text}")
    for idx, answer in enumerate(answers, 1):
        question_text = Question.query.get(answer.question_id).text
        click.echo(f"{idx}: {answer.text} - Correct: {answer.is_correct}")


@answer_cli.command("delete")
@click.argument("answer_id")
def delete_answer(answer_id):
    """Delete an answer."""
    answer = Answer.query.get(answer_id)
    if answer:
        db.session.delete(answer)
        db.session.commit()
        click.echo(f"Answer '{answer.text}' deleted successfully.")
    else:
        click.echo(f"Answer with ID {answer_id} not found.")


# User CLI group
user_cli = AppGroup("user")


@user_cli.command("add")
@click.option("--username", prompt=True, help="The username of the user.")
@click.option(("--email"), prompt=True, help="The email of the user.")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="The password of the user.")
@click.option("--is_admin", prompt=True, type=bool, help="Whether the user is an admin.")
def add_user(username, email, password, is_admin):
    """Add a new user."""
    from app import bcrypt

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password_hash=hashed_password, is_admin=is_admin)
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

    for user in users:
        click.echo(f"{user.id}: {user.username} - {user.email} - Admin: {user.is_admin}")
    
@user_cli.command("list_admin")
def list_admins():
    """List all admins."""
    admins = User.query.filter_by(is_admin=True).all()
    if not admins:
        click.echo("No admins found.")
        return
    click.echo("Admins:")
    click.echo("-" * 100)
    for admin in admins:
        click.echo(f"{admin.id}: {admin.username} - {admin.email} - Admin: {admin.is_admin}")


@user_cli.command("delete")
@click.argument("user_id")
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        click.echo(f"User '{user.username}' deleted successfully.")
    else:
        click.echo(f"User with ID {user_id} not found.")
