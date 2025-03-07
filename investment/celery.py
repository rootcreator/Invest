import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investment.settings")

app = Celery("investment")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "calculate_weekly_profits_every_sunday": {
        "task": "core.tasks.calculate_weekly_profits",
        "schedule": crontab(minute=0, hour=0, day_of_week="sunday"),  # Every Sunday at midnight
    },

    'core.tasks.calculate_monthly_profits': {
        'task': 'core.tasks.calculate_monthly_profits',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),
    },
}