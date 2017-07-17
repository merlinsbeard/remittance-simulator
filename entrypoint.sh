#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
echo Starting Gunicorn.
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --name docker_mayannah \
    --workers 2 \
    --log-level=info \
    --access-logfile - \
"$@"
echo ohmmm
