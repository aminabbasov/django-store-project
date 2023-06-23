import os

from django.conf import settings

from app.conf.environ import env


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#* STATIC_URL = "static/"

#! STATIC_ROOT = env("STATIC_ROOT", cast=str, default="static")

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(settings.BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'static', 'images')

MEDIA_URL = '/images/'
