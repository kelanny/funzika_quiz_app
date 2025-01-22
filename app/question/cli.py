#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.question.models import Question
from app.quiz.models import Quiz


# Question CLI group
question_cli = AppGroup("question")


@question_cli.command("add")
@click.option("--text", required=True, help="The question text.")
@click.option("--quiz_id", required=True, help='Reference to the quiz id.')
@click.option("--score", required=True, type=int, help='Score for this question.')
def add_question(text, quiz_id, score):
    """Add a new question."""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        click.echo("No quiz was found.")
    question = Question(text=text, quiz_id=quiz.id, score=score)
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
        click.echo(f"Question: ({idx})")
        click.echo(f"Question ID: {question.id}")
        click.echo(f"Text: {question.text}")
        click.echo(f"Score: {question.score}")
        click.echo("Answers:")
        for answer in question.answers:
            click.echo(
                f"\t- {answer.id}"
                f"\t- {answer.text}"
                f"\t{'(Correct)' if answer.is_correct else ''}"
                )
        click.echo("-" * 100)
        click.echo()

@question_cli.command("view")
@click.argument("question_id")
def view_question(question_id):
    """View a question."""
    question = Question.query.get(question_id)
    if question:
        click.echo(f"Question ID: {question.id}")
        click.echo(f"Text: {question.text}")
        click.echo(f"Score: {question.score}")
        click.echo("Answers:")
        for answer in question.answers:
            click.echo(
                f"\t- {answer.id}"
                f"\t- {answer.text}"
                f"\t{'(Correct)' if answer.is_correct else ''}"
                )
    else:
        click.echo(f"Question with ID {question_id} not found.")

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
