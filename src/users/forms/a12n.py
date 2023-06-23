from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from users.forms import NameValidatorMixin
from users.models import User


class UsersRegisterForm(UserCreationForm, NameValidatorMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "John",
                'form': "RegisterForm",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "Doe",
                'form': "RegisterForm",
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "johndoe",
                'form': "RegisterForm",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': "example@email.com",
                'form': "RegisterForm",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'form': "RegisterForm",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'form': "RegisterForm",
            }
        )
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UsersLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "johndoe",
                'form': "LoginForm",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'form': "LoginForm",
            }
        )
    )


class UsersPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Current Password",
                'form': "PasswordChangeForm",
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "New password",
                'form': "PasswordChangeForm",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Confirm password",
                'form': "PasswordChangeForm",
            }
        )
    )
