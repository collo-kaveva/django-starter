#!/bin/bash
set -e

echo "Starting Django application startup sequence..."

# Wait for database to be ready (if DATABASE_URL is set)
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database to be ready..."
    # Extract host from DATABASE_URL and wait for it
    # This is a simple wait - for production you might want a more sophisticated check
    sleep 2
fi

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create/update Django Site object if ALLOWED_HOSTS is set
if [ -n "$ALLOWED_HOSTS" ]; then
    echo "Updating Django Site object..."
    python manage.py shell -c "
from django.contrib.sites.models import Site
import os

# Get the first allowed host
allowed_hosts = os.environ.get('ALLOWED_HOSTS', '').split(',')
if allowed_hosts:
    domain = allowed_hosts[0].strip()
    site, created = Site.objects.get_or_create(id=1)
    site.domain = domain
    site.name = domain
    site.save()
    print(f'Site object {\"created\" if created else \"updated\"}: {domain}')
"
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --access-logfile - \
    --error-logfile - \
    "$@"
