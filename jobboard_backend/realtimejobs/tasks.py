from realtimejobs.models import JobAlert, JobPost
from realtimejobs.queries.job_alert_queries import JobAlertQueries
from celery import shared_task  # type: ignore
from django.core.mail import send_mail, send_mass_mail  # type: ignore
from django.conf import settings  # type: ignore
from collections import defaultdict
from django.db.models import Q # type: ignore
from django.utils import timezone # type: ignore



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


@shared_task
def send_periodic_job_alerts():
    """Efficiently fetch job alerts and send batch emails to thousands of users."""

    alerts = JobAlert.objects.filter(is_active=True).prefetch_related('categories', 'job_types')
    print(f"Found {alerts.count()} active job alerts.")

    # Fetch all job posts once, reducing repetitive queries
    all_jobs = JobPost.objects.all().order_by('-created_at')[:100]  # Fetch 100 latest jobs in bulk

    # Categorize jobs based on category, job type, and location
    categorized_jobs = defaultdict(list)

    for job in all_jobs:
        categorized_jobs[(job.category_id, job.job_type_id, job.location)].append(job)
        if job.is_worldwide:
            categorized_jobs[(job.category_id, job.job_type_id, None)].append(job)  # Handle worldwide jobs

    email_messages = []

    for alert in alerts:
        print(f"Processing alert for: {alert.email}")

        user_categories = alert.categories.values_list('id', flat=True)
        user_job_types = alert.job_types.values_list('id', flat=True)

        jobs = [
            job for (category_id, job_type_id, location), job_list in categorized_jobs.items()
            if category_id in user_categories and job_type_id in user_job_types and (alert.location == location or location is None)
        ]

        # If no matching jobs, fetch the latest ones
        if not jobs:
            jobs = list(all_jobs[:5])  # Fallback to latest 5 jobs

        if jobs:
            subject = f"🔥 RealtimeJobs New Job Alert - {timezone.now().strftime('%b %d, %Y')}"

            job_list_text = "\n\n".join(
                f"{job.title}\n{job.short_description}\nLocation: {job.location}\nLink: https://yourwebsite.com/jobs/{job.slug}"
                for job in jobs[:5]  # Limit to 5 per user
            )

            message = f"""Hello {alert.user.full_name},

Here are the latest job postings for you:
{job_list_text}

View more jobs here: https://yourwebsite.com/jobs

To unsubscribe, click here: https://yourwebsite.com/unsubscribe/{alert.id}

Best,
RealtimeJobs Team
            """

            email_messages.append((subject, message, settings.EMAIL_HOST_USER, [alert.email]))

    if email_messages:
        send_mass_mail(email_messages, fail_silently=False)
        print(f"✅ Sent {len(email_messages)} job alert emails successfully.")

    print("📬 Job alert task completed.")
