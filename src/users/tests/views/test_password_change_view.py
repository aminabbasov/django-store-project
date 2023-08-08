import pytest

from django.urls import reverse

from users.tests.factories import UsersPasswordChangeFormFactory


pytestmark = [pytest.mark.django_db]


def test_password_change_view_invalid_form_post_method(client):
    url = reverse("users:change-password")
    response = client.post(url)
    assert response.status_code == 302


def test_password_change_view_valid_form_post_method(client):
    url = reverse("users:change-password")
    data = UsersPasswordChangeFormFactory().data
    response = client.post(url, data=data)
    assert response.status_code == 302
