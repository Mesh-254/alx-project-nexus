import os
from celery import Celery
from celery.schedules import crontab #type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobboard_backend.settings")


app = Celery("jobboard_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()


# periodic task schedule using Celery Beat
app.conf.beat_schedule = {
    "send-job-alerts-every-24-hours": {
        "task": "realtimejobs.tasks.send_periodic_job_alerts",
        "schedule": crontab( minute="*"),  # Runs daily at 8 AM
    },
}

