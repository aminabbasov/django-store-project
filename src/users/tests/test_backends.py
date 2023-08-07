import pytest

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from users.backends import UsernameOrEmailModelBackend


@pytest.mark.django_db
def test_username_or_email_model_backend(mixer, rf):
    user = mixer.blend("users.User", username="foo", password=make_password("bar"))
    result = (
        UsernameOrEmailModelBackend()
        .authenticate(
            request=rf.post(reverse("users:login")),
            username=user.username,
            password="bar",
        )
    )
    assert result == user
