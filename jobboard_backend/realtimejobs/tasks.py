from celery import shared_task #type: ignore
from django.core.mail import send_mail #type: ignore
from django.urls import reverse #type: ignore
from django.conf import settings #type: ignore
from .models import JobAlert


@shared_task
def send_subscription_email(job_alert_id):
    """Sends a confirmation email when a user subscribes to job alerts."""
    job_alert = JobAlert.objects.get(id=job_alert_id)

    # unsubscribe_url = f"https://yourwebsite.com{reverse('unsubscribe', args=[job_alert.id])}"
    subject = "You're Subscribed to RealtimeJobs Alerts!"
    message = f"""
    Hi {job_alert.user.full_name},

    You have successfully subscribed to RealtimeJob job alerts. We will send you job updates based on your preferences.

    If you ever want to unsubscribe, click the link below:
    # 

    Best,
    Realtimejobs Board Team
    """

    send_mail(subject, message, settings.EMAIL_HOST_USER, [job_alert.email])
