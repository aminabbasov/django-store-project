import pytest

from faker import Faker

from django.urls import reverse


@pytest.fixture
def mail_data():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "subject": fake.sentence(nb_words=10),
        "message": fake.text(),
    }


def test_contact_view_get_method(client):
    url = reverse("products:contact")
    response = client.get(url)
    assert response.status_code == 200


def test_contact_view_valid_post_method(client, mail_data):
    url = reverse("products:contact")
    response = client.post(url, mail_data)
    assert response.status_code == 200
