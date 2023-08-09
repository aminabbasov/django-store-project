from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Callable, TypeAlias

from django.apps import apps
from django.db.models import Q
from django.db.models import QuerySet

from app.services import BaseService
from users.models import User


username: TypeAlias = str


@dataclass
class UserUpdater(BaseService):
    user: User | username | QuerySet[User]
    user_data: dict

    def act(self) -> User:
        return self.update(self.user, self.user_data)

    def _if_user_is_queryset(self) -> None:
        if isinstance(self.user, QuerySet):
            if count := self.user.count() == 1:
                self.user = self.user.first()
            elif count == 0:
                raise AttributeError("You passed an empty QuerySet, but it must consist of a single object")
            else:
                raise AttributeError("You passed a QuerySet of multiple objects, but only one is expected")

    def get_validators(self) -> list[Callable]:
        return [self._if_user_is_queryset]

    @singledispatchmethod
    def update(self, user, user_data):
        raise NotImplementedError("Add dispatch methods")

    @update.register(User)
    def _(self, user: User, user_data: dict) -> User:
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value or getattr(user, key))
            else:
                raise AttributeError(f"{user} has no field named '{key}'")

        user.save()
        return user

    @update.register(username)
    def _(self, user: username, user_data: dict) -> User:
        obj = apps.get_model("users.User").objects.filter(username=user)  # because .update() works only with QuerySet
        obj.update(**user_data)

        if obj.first() is None:
            query = Q(username=user_data.get("username", "")) | Q(email=user_data.get("email", ""))
            return apps.get_model("users.User").objects.get(query)

        return obj.first()  # to return User, not QuerySet
