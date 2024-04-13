# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coded.settings')

# app = Celery('coded')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# celery.py

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coded.settings')

app = Celery('coded')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat configuration for periodic tasks scheduling
app.conf.beat_schedule = {
    'send-sms-every-2-minutes': {
        'task': 'modern.tasks.process_payment_rows',  # Task name to schedule
        'schedule': crontab(minute='*/2'),  # Run every 2 minutes
    },
}