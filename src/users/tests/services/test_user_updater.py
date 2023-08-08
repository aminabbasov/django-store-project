import pytest

from users.models import User
from users.services import UserUpdater


pytestmark = [pytest.mark.django_db]


def test_user_updater_if_user_isobject(mixer, user_data):
    user = mixer.blend("users.User")
    assert isinstance(UserUpdater(user, user_data)(), User)


def test_user_updater_if_user_is_username(mixer, user_data):
    user = mixer.blend("users.User", username="example")
    assert isinstance(UserUpdater(user.username, user_data)(), User)
    # Warning: for some reason .update(**user_data) clears queryset


def test_user_updater_if_user_is_queryset(mixer, user_data):
    user = mixer.blend("users.User", username="example")
    queryset = User.objects.filter(username=user.username)
    assert isinstance(UserUpdater(queryset, user_data)(), User)


def test_user_updater_if_empty_queryset(user_data):
    queryset = User.objects.filter(username="NO_USER")

    with pytest.raises(AttributeError):
        UserUpdater(queryset, user_data)()


def test_user_updater_if_multiple_objects_queryset(mixer, user_data):
    mixer.cycle(2).blend("users.User", first_name="foo")

    queryset = User.objects.filter(username="foo")

    with pytest.raises(AttributeError):
        UserUpdater(queryset, user_data)()


def test_user_updater_if_user_data_has_unknown_attr(mixer, user_data):
    user = mixer.blend("users.User")
    user_data["UNKNOWN"] = "attribute"

    with pytest.raises(AttributeError):
        UserUpdater(user, user_data)()


def test_user_updater_if_user_not_supported_by_singledispatch(user_data):
    dummy = type("DummyObject", (), {})

    with pytest.raises(NotImplementedError):
        UserUpdater(dummy, user_data)()
