from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from loguru import logger
from a_messageboard.models import MessageBoard
from django.template.loader import render_to_string
from datetime import datetime

@shared_task(name='email_notification')
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
        
    return recipient_email


@shared_task(name="monthly_newsletter")
def send_newsletter():
    subject = "Your Monthly Newsletter"
    subscribers = MessageBoard.objects.get(id=4).subscribers.all()

    for subscriber in subscribers:
        body = render_to_string('a_messageboard/newsletter.html', {})
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.content_subtype = "html"
        email.send()
    
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()
    
    return f'{current_month} NNewsletter sent to {subscriber_count} subs.'
    
