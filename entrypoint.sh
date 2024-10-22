#!/bin/sh

# Activate the virtual environment
. /app/.venv/bin/activate

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Run the application
exec "$@"
