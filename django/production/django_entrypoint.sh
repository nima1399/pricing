#!/bin/sh
set -e  # Exit immediately if any command fails

echo "Running migrations..."
uv run -- python manage.py migrate

echo "Starting server..."
exec "$@"  # This runs the CMD arguments (the runserver command)
