#!/bin/bash

# Terminate Gunicorn
echo "Stopping Gunicorn..."
#pkill -f "gunicorn --workers 3 --bind unix:/home/bob/code/coded.sock coded.wsgi:application"

# Terminate Celery Worker
echo "Stopping Celery Worker..."
pkill -f "celery -A modern worker --loglevel=info"

# Terminate Celery Beat
echo "Stopping Celery Beat..."
pkill -f "celery -A modern beat --loglevel=info"

echo "Gunicorn and Celery stopped."
