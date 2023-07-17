# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from app.conf.environ import env


DATABASES = {
    # read os.environ["DATABASE_URL"] and raises ImproperlyConfigured exception if not found
    "default": env.db(),
}
DATABASES["default"]["OPTIONS"] = {'options': '-c search_path=shop,public'}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not env("DEBUG", cast=bool):
    DATABASES["default"]["CONN_MAX_AGE"] = 600
