import pytest

from users.models import User
from users.services import UserCreator


@pytest.mark.django_db
def test_user_creator(user_data):
    assert isinstance(UserCreator(**user_data)(), User)
