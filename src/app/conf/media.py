import os

from django.conf import settings


MEDIA_ROOT = os.path.join(settings.BASE_DIR, "static", "images")

MEDIA_URL = "/images/"
