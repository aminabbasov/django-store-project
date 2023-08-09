import pytest
from random import randint

from django.contrib.auth.hashers import make_password
from django.urls import reverse

from users.tests.factories import UsersLoginFormFactory


def test_login_view_get_method(client):
    url = reverse("users:login")
    response = client.get(url)
    assert response.status_code == 200


def test_login_view_invalid_form_post_method(client):
    url = reverse("users:login")
    response = client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_valid_form_with_username_post_method(mixer, client):
    url = reverse("users:login")
    data = UsersLoginFormFactory(username_or_email="user_name").data
    mixer.blend("users.User", username=data["username"], password=make_password(data["password"]))
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_valid_form_with_email_post_method(mixer, client):
    url = reverse("users:login")
    data = UsersLoginFormFactory(username_or_email="email").data
    mixer.blend("users.User", email=data["username"], password=make_password(data["password"]))
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_valid_form_with_random_post_method(mixer, client):
    url = reverse("users:login")
    data = UsersLoginFormFactory().data

    if randint(0, 1):
        mixer.blend("users.User", username=data["username"], password=make_password(data["password"]))
    else:
        mixer.blend("users.User", email=data["username"], password=make_password(data["password"]))

    response = client.post(url, data=data)
    assert response.status_code == 302
