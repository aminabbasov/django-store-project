# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

from django.urls import reverse_lazy


AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = ["users.backends.UsernameOrEmailModelBackend"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_REDIRECT_URL = reverse_lazy("users:account")

LOGIN_URL = reverse_lazy("users:login")

LOGOUT_URL = reverse_lazy("users:logout")


# Using plain bcrypt for password storage.
#
# Avoiding Django's default pre-hashing (BCryptSHA256PasswordHasher) for compatibility with
# other hashing libraries like Ruby Devise or Laravel's default algorithm.
#
# Note: Passwords can't exceed 72 characters due to this choice.

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]
