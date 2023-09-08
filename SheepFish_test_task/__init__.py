import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SheepFish_test_task.settings")

app = Celery("SheepFish_test_task")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
