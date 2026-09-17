#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Seeding default products..."
python manage.py seed_products || true

echo "Starting Gunicorn server..."
exec gunicorn sale_ai.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
