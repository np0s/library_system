#!/usr/bin/env bash
set -e

# Wait for any dependent services if needed (placeholder)
# ...existing code...

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# If a custom command was provided, run it; otherwise default CMD in Dockerfile will run
if [ "${1:0:1}" = '-' ]; then
    exec "$@"
else
    exec "$@"
fi