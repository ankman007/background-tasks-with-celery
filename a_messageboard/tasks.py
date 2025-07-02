from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from loguru import logger

@shared_task
def send_email(recipient_email, message, author):
    try:
        subject = f"New message from {author} on a messageboard you're subscribed to"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False
        )
    except Exception as e:
        logger.exception(f"[EMAIL TASK] Failed to send email to {recipient_email}: {str(e)}")
