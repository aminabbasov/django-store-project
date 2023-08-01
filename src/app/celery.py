import os

from celery import Celery
from django.conf import settings

from app.conf.environ import env


__all__ = [
    "celery",
]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("app")

celery.conf.update(
    broker_url=env('REDIS_URL'),
    broker_transport_options={'visibility_timeout': 3600},
    broker_connection_retry_on_startup=True,
    result_backend=env('REDIS_URL'),
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
)

celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
