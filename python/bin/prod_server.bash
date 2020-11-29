#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python /app/manage.py collectstatic --noinput

gunicorn config.wsgi --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=config.settings.production --chdir=/app
