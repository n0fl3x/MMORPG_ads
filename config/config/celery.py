import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_non_active_users_and_codes_clear': {
        'task': 'accounts.tasks.weekly_non_active_users_and_codes_clear',
        'schedule': crontab(hour=18, minute=38, day_of_week='thursday'),
        'args': (),
    },
}
