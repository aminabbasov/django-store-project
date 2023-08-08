import pytest

from django.urls import reverse

from checkout.tests.factories import CheckoutOrderCreateFormFactory


def test_checkout_view_get_method(client):
    url = reverse("checkout:checkout")
    response = client.get(url)
    assert response.status_code == 200


def test_checkout_view_form_invalid_post_method(client):
    url = reverse("checkout:checkout")
    response = client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_view_form_valid_anonymous_user_post_method(client):
    url = reverse("checkout:checkout")
    data = CheckoutOrderCreateFormFactory().data
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_checkout_view_form_valid_authorized_user_post_method(client, user):
    url = reverse("checkout:checkout")
    data = CheckoutOrderCreateFormFactory().data
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302
