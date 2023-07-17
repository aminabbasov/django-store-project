from django.conf import settings


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

APPS = [
    # "app",
    # "a12n",
    # "users",

    "app",
    
    "users",
    "products",
    "checkout",
]

THIRD_PARTY_APPS = [
    # "drf_spectacular",
    # "drf_spectacular_sidecar",
    # "rest_framework",
    # "rest_framework.authtoken",
    # "rest_framework_jwt.blacklist",
    # "django_filters",
    # "axes",
]

if settings.DEBUG:
    THIRD_PARTY_APPS += [
        "debug_toolbar",
    ]

INSTALLED_APPS = DJANGO_APPS + APPS + THIRD_PARTY_APPS
