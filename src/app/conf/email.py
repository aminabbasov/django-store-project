from app.conf.environ import env

from email.utils import getaddresses


# Email settings
# https://django.fun/ru/docs/django/4.1/topics/email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # django.core.mail.backends.console.EmailBackend

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'

EMAIL_USE_TLS = True

EMAIL_PORT = '2525'

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = env.str('EMAIL_HOST_USER')

ADMINS = getaddresses([env('ADMINS')])
