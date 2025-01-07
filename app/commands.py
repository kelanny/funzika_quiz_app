#!/usr/bin/env python
"""CLI commands for the application."""

import click
from flask.cli import AppGroup
from app import db
from app.user.models import User


# User CLI group
user_cli = AppGroup("user")
