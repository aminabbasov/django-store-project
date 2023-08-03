from app.conf.environ import env

if env("NO_CACHE", cast=bool, default=False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    }
else:
    CACHES = {
        "default": env.cache("REDIS_URL"),
    }

REDIS_URL = env("REDIS_URL")  # for "django-health-check" package

CACHE_TTL = 10
