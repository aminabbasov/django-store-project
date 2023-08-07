import re
from random import choice

import factory
from pytest_factoryboy import register
from mixer.backend.django import mixer

from django.contrib.auth.hashers import make_password

from app.test import BaseFormFactory
from users.forms import UsersRegisterForm, UsersLoginForm, UsersAccountForm, UsersPasswordChangeForm


@register
class UsersRegisterFormFactory(BaseFormFactory):
    class Meta:
        model = UsersRegisterForm
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password1 = factory.Faker('password')
    password2 = factory.LazyAttribute(lambda o: o.password1)


@register
class UsersLoginFormFactory(BaseFormFactory):
    class Meta:
        model = UsersLoginForm        

    username = factory.Faker("user_name")  # TODO: add email
    password = factory.Faker('password')


@register
class UsersAccountFormFactory(BaseFormFactory):
    class Meta:
        model = UsersAccountForm
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')


@register
class UsersPasswordChangeFormFactory(BaseFormFactory):
    class Meta:
        model = UsersPasswordChangeForm
    
    @classmethod
    def init_params(cls):
        return {"user": mixer.blend("users.User", password=make_password("12345678"))}
    
    old_password = "12345678"
    new_password1 = factory.Faker('password')
    new_password2 = factory.LazyAttribute(lambda o: o.new_password1)
