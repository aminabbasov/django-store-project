from django.conf import settings


DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CUSTOM_MIDDLEWARE = [
    'checkout.middleware.BasketMiddleware',
]

THIRD_PARTY_MIDDLEWARE = [
    
]

if settings.DEBUG:
    THIRD_PARTY_MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

MIDDLEWARE = DJANGO_MIDDLEWARE + CUSTOM_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE
