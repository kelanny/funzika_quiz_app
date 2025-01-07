#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.user.models import User


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

    for user in users:
        click.echo(f"{user.id}: {user.username} - \
                   {user.email} - Admin: {user.is_admin}")


@user_cli.command("list-admin")
def list_admins():
    """List all admins."""
    admins = User.query.filter_by(is_admin=True).all()
    if not admins:
        click.echo("No admins found.")
        return
    click.echo("Admins:")
    click.echo("-" * 100)
    for admin in admins:
        click.echo(f"{admin.id}: {admin.username} - \
                   {admin.email} - Admin: {admin.is_admin}")


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

@user_cli.command("view")
@click.argument('email')
def view_user(email):
    user = User.query.get(email)
    if not user:
        click.echo(f'User {email} was not found.')
    # click.echo(f"User ID: {user.id}\nUsername: {user.username}\nEmail: {user.email}")
    click.echo(f"{user}")