#!/bin/bash

# Start Gunicorn
echo "Starting Gunicorn..."
#gunicorn --workers 3 --bind unix:/home/bob/code/coded.sock coded.wsgi:application > /var/log/gunicorn.log 2>&1 &

# Start Celery Worker
echo "Starting Celery Worker..."
celery -A modern worker --loglevel=info > /home/bob/code/logs/celery_worker.log 2>&1 &

# Start Celery Beat (Optional)
echo "Starting Celery Beat..."
celery -A modern beat --loglevel=info > /home/bob/code/logs/celery_beat.log 2>&1 &

echo "Gunicorn and Celery started."


gunicorn --workers 3 --bind unix:/home/bob/code/coded.sock coded.wsgi:application &
celery -A modern worker --loglevel=info &
celery -A modern beat --loglevel=info &
