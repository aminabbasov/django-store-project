import pytest

from django.urls import reverse

from users.tests.factories import UsersAccountFormFactory


def test_account_edit_view_invalid_form_post_method(client):
    url = reverse("users:edit-account-details")
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_account_edit_view_valid_form_post_method(client):
    url = reverse("users:edit-account-details")
    data = UsersAccountFormFactory().data
    response = client.post(url, data=data)
    assert response.status_code == 302
