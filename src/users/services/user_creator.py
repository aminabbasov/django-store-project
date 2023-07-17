from dataclasses import dataclass

from app.services import BaseService
from users.forms import UsersRegisterForm


@dataclass
class UserCreator(BaseService):
    first_name: str
    last_name: str
    username: str
    email: str
    password1: str
    password2: str

    def act(self):
        ...
        
    def create(self):
        UsersRegisterForm()
    
    