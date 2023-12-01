from django.conf import settings


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

APPS = [
    "app",
    "users",
    "products",
    "checkout",
]

THIRD_PARTY_APPS = [
    "health_check",
    "health_check.db",
    "health_check.contrib.migrations",
    "health_check.contrib.redis",
    "health_check.contrib.celery_ping",
]

if settings.DEBUG:
    THIRD_PARTY_APPS += [
        "debug_toolbar",
    ]

INSTALLED_APPS = DJANGO_APPS + APPS + THIRD_PARTY_APPS
