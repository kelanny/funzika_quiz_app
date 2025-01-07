#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.question.models import Question


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
