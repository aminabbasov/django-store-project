from typing import Union

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager

from app.models import models


class UserManager(_UserManager):
    def is_username_available(self, username: str) -> bool:
        return not self.filter(username=username).exists()

    def get_by_username(self, username: str) -> Union["User", None]:  # "User" | None gives TypeError
        return self.get(username=username) or None


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True, max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    # Only 15 because of  ITU-T E. 164 - (https://www.itu.int/rec/T-REC-E.164-201011-I/en)
    # "A.3.5 - Summary of number length" says that maximum number length is 15 digits.

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        # unique_together = [['username', 'email']]
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"],
                # condition=models.Q(unique=True),
                name="username_and_email_unique",
            )
        ]
