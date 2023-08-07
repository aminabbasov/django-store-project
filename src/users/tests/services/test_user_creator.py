import pytest

from users.services import UserCreator
from users.models import User


@pytest.mark.django_db
def test_user_creator(user_data):
    assert isinstance(UserCreator(**user_data)(), User)
