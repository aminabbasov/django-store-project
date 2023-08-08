from datetime import timedelta


BASKET_SESSION_ID = "basket"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

KEEP_LOGGED_DURATION = timedelta(days=365)
