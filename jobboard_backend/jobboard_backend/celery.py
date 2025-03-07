import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobboard_backend.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()