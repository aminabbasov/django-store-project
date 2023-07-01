from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import UserManager as _UserManager

from app.models import models


class UserQuerySet(models.QuerySet):
    def is_username_available(self, username):
        return not self.filter(username=username).exists()

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, max_length=255)
    phone_number = models.CharField(max_length=100, unique=True, blank=True)
    
    objects = UserQuerySet.as_manager()
    
    class Meta(AbstractUser.Meta):
        # unique_together = [['username', 'email']]
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], 
                # condition=models.Q(unique=True),
                name='username_and_email_unique'
            )
        ]
