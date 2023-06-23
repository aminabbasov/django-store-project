from django import forms

from users.forms import NameValidatorMixin


class WebsiteAccountForm(forms.Form, NameValidatorMixin):
    def __init__(self, user, *args, **kwargs):
        super(WebsiteAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = getattr(user, 'first_name', '')
        self.fields['last_name'].widget.attrs['placeholder'] = getattr(user, 'last_name', '')
        self.fields['username'].widget.attrs['placeholder'] = getattr(user, 'username', '')
        self.fields['email'].widget.attrs['placeholder'] = getattr(user, 'email', '')
        self.fields['phone_number'].widget.attrs['placeholder'] = getattr(user, 'phone_number', '')
    
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "John",
                'form': "WebsiteAccountEditForm",
            }
        )
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "Doe",
                'form': "WebsiteAccountEditForm",
            }
        )
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "johndoe",
                'form': "WebsiteAccountEditForm",
            }
        )
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': "example@email.com",
                'form': "WebsiteAccountEditForm",
            }
        )
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "+123 456 789",
                'form': "WebsiteAccountEditForm",
            }
        )
    )
