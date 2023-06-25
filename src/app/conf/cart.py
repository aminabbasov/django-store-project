from datetime import timedelta


CART_SESSION_ID = 'cart'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

KEEP_LOGGED_DURATION = timedelta(days=365)
