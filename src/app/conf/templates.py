import os

from django.conf import settings


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(settings.BASE_DIR, "templates"),
            os.path.join(settings.BASE_DIR, "app", "admin", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # my context processors
                "checkout.context_processors.basket",
            ],
        },
    },
]
