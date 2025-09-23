from __future__ import absolute_import,unicode_literals
import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev') 

app = Celery('flowcash')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'print_test_celery': {
        'task': 'expenses.tasks.test_task',
        'schedule': 30.0,
    }
}
app.autodiscover_tasks()