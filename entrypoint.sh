#!/bin/sh

# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Apply database migrations
python manage.py migrate

# Start the server
exec "$@"
