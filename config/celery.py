from __future__ import absolute_import,unicode_literals
import os 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev') 

app = Celery('flowcash')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'print_test_celery': {
        'task': 'apps.expenses.tasks.creating_recurring_costs',
        'schedule': crontab(hour=0,minute=0),
    }
}
app.autodiscover_tasks()