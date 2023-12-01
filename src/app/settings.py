"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from split_settings.tools import include

from django.conf import settings

from app.conf.environ import env


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", cast=str, default="s3cr3t")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)
CI = env("CI", cast=bool, default=False)

include(
    "conf/auth.py",
    "conf/boilerplate.py",
    "conf/db.py",
    "conf/http.py",
    "conf/i18n.py",
    "conf/installed_apps.py",
    "conf/media.py",
    "conf/middleware.py",
    "conf/static.py",
    "conf/templates.py",
    "conf/timezone.py",
    "conf/basket.py",
    "conf/email.py",
    "conf/cache.py",
)

if settings.DEBUG:
    include("conf/debug_toolbar.py")
