#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.answer.models import Answer
from app.question.models import Question

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
        click.echo(f"{idx}: Question ID: ({answer.question_id}) Answer ID: ({answer.id}) {answer.text} - Correct: {answer.is_correct}")


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
