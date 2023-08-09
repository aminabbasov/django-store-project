from dataclasses import dataclass

from app.services import BaseService
from users.models import User


@dataclass
class UserCreator(BaseService):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    def act(self) -> User:
        return self.create()

    def create(self) -> User:
        return User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            password=self.password,
        )
