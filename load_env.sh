#!/usr/bin/env bash
# Loads Funzika app environment variables

read -p "Enter your app environment: " environ

export FLASK_ENV="$environ"

export FLASK_APP=run.py

echo "Environment variables set successfully."

echo "Funzika App Environment: $FLASK_ENV"
echo "Funzika APP: $FLASK_APP"

