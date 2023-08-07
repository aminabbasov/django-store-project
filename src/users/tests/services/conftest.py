import pytest


@pytest.fixture
def user_data():
    return {
        "first_name": "test",
        "last_name": "user",
        "username": "testuser",
        "email": "test@user.com",
        "password": "test",
    }
