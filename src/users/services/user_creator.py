from dataclasses import dataclass

from users.models import User
from app.services import BaseService


@dataclass
class UserCreator(BaseService):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    def act(self) -> User:
        user = self.create()
        return user
        
    def create(self) -> User:
        user = User.objects.create_user(
            first_name= self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            password=self.password,
        )
        return user
    
    