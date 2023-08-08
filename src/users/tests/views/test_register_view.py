import pytest

from django.urls import reverse

from users.tests.factories import UsersRegisterFormFactory


def test_register_view_get_method(client):
    url = reverse("users:register")
    response = client.get(url)
    assert response.status_code == 200


def test_register_view_invalid_form_post_method(client):
    url = reverse("users:register")
    response = client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_valid_form_post_method(client):
    url = reverse("users:register")
    data = UsersRegisterFormFactory().data
    response = client.post(url, data=data)
    assert response.status_code == 302
