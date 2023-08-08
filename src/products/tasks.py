from django.conf import settings
from django.core.mail import send_mail as _send_mail

from app.celery import celery


@celery.task
def send_mail(name, email, subject, message):
    body = f"""
        You have received a new message from your website contact form.\n\n
        Here are the details:\n\n
        Name: {name}\n\n
        Email: {email}\n\n
        Subject: {subject}\n\n
        Message: {message}
    """
    _send_mail(subject, body, email, [email for name, email in settings.ADMINS], fail_silently=False)
