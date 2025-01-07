#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.quiz.models import Quiz
from app.question.models import Question
from app.answer.models import Answer


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
        click.echo(f"{quiz.id}: {quiz.title} - \
                   {quiz.description} - Active: {quiz.is_active}")


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
                    click.echo(f"\t- {answer.text} - \
                               Correct: {answer.is_correct}")
                click.echo("-" * 100)
                click.echo()

    else:
        click.echo(f"Quiz with ID {quiz_id} not found.")
