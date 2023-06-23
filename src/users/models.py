from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import UserManager as _UserManager

from app.models import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, max_length=255)
    phone_number = models.CharField(max_length=100, unique=True, blank=True)
    
    from django.contrib.auth.models import Group, Permission                               #! TYT TYT TYT TYT TYT TYT TYT TYT TYT
    groups = models.ManyToManyField(Group, related_name="custom_user_set")                 #! TYT *ибо сейчас нет базы данных TYT
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set")  #! TYT TYT TYT TYT TYT TYT TYT TYT TYT
    
    class Meta(AbstractUser.Meta):
        # unique_together = [['username', 'email']]
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], 
                # condition=models.Q(unique=True),
                name='username_and_email_unique'
            )
        ]
