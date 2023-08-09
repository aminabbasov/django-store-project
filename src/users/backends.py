from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


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
                Q(**{f"{user_model.USERNAME_FIELD}__iexact": username}) | Q(email__iexact=username)
            )
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
