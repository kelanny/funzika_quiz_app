#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from dummy_data.populate_quiz import create_dummy_quizzes


# User CLI group
populate_cli = AppGroup("populate")

@populate_cli.command("quizzes")
@click.option("--num_quizzes", default=5, type=int, help="Number of quizzes to create.")
@click.option("--num_questions_per_quiz", default=10, type=int, help="Number of questions to create per quiz.")
def populate_quizzes(num_quizzes, num_questions_per_quiz):
    """Populate the database with dummy quizzes and questions."""
    create_dummy_quizzes(num_quizzes, num_questions_per_quiz)
    click.echo("Dummy quizzes and questions created successfully.")

