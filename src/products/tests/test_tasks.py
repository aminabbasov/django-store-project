import pytest
import faker

from django.core import mail

from products.tasks import send_mail


@pytest.fixture
def mail_data():
    fake = faker.Faker()
    return {
        "name": fake.name(),
        "email": 'from@example.com',
        "subject": fake.sentence(),
        "message": fake.text(),
    }


def test_send_mail(mail_data):
    send_mail(**mail_data)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].from_email == 'from@example.com'
