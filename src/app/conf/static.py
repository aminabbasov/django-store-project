import os

from django.conf import settings

from app.conf.environ import env


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = env("STATIC_ROOT", cast=str, default=os.path.join(settings.BASE_DIR, "staticfiles"))

STATICFILES_DIRS = [
    os.path.join(settings.BASE_DIR, "static"),
    os.path.join(settings.BASE_DIR, "app", "admin", "static"),
]
