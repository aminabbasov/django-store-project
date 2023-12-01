from email.utils import getaddresses

from app.conf.environ import env


# Email settings
# https://django.fun/ru/docs/django/4.1/topics/email

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

EMAIL_HOST = env("EMAIL_HOST", default="localhost")

EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)

EMAIL_PORT = env("EMAIL_PORT", default="25")

EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")

EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

ADMINS = getaddresses([env("ADMINS", default="admin@admin.com")])
