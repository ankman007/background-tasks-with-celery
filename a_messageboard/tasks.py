from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from loguru import logger

@shared_task
def send_email(recipient_email, message, author):
    subject = f"New message from {author} on a messageboard you're subscribed to"

    logger.info(f"[EMAIL TASK] Preparing to send email to {recipient_email}")
    logger.debug(f"[EMAIL TASK] Subject: {subject}")
    logger.debug(f"[EMAIL TASK] Message content:\n{message}")

    try:
        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False  # Set to False for error visibility
        )

        if sent_count == 1:
            logger.success(f"[EMAIL TASK] Email successfully sent to {recipient_email}")
        else:
            logger.warning(f"[EMAIL TASK] Email not sent to {recipient_email}. send_mail returned: {sent_count}")

    except Exception as e:
        logger.exception(f"[EMAIL TASK] Failed to send email to {recipient_email}: {str(e)}")
