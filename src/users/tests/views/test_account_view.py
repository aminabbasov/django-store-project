import pytest

from django.urls import reverse


@pytest.fixture
def user(mixer):
    return mixer.blend("users.User")


def test_account_view_anonymous_user_get_method(client):
    url = reverse('users:account')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_account_view_authorized_user_get_method(client, user):
    url = reverse('users:account')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
