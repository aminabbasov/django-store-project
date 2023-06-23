# import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


#! logger = logging.getLogger(__name__)

class UsernameOrEmailModelBackend(ModelBackend):
    """
    Custom authentication Backend for login using email or username 
    with password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        if username is None or password is None:
            return

        try:
            user = user_model.objects.get(
                Q(**{f'{user_model.USERNAME_FIELD}__iexact': username}) | Q(email__iexact=username)
            )
        except user_model.DoesNotExist:
            #! logger.warning('Authentication warning: user does not exist.', exc_info=True)
            user_model().set_password(password)
        #! except Exception:
            #! logger.error('Authentication error.', exc_info=True)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
