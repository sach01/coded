# from __future__ import absolute_import, unicode_literals
# import os

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coded.settings')

# app = Celery('coded')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coded.settings')

app = Celery('coded')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.schedules import crontab
# Celery Beat configuration for periodic tasks scheduling
app.conf.beat_schedule = {
    'send_monthly_sms': {
        'task': 'modern.tasks.send_monthly_sms',  # Task name to schedule
        'schedule': crontab(minute='*/2'),  # Run every 2 minutes
    },
}
