from django import forms

from checkout.models import Order


class CheckoutOrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "country",
            "city",
            "state",
            "zip_code",
            "price",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "John",
                    "form": "OrderForm",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Doe",
                    "form": "OrderForm",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@email.com",
                    "form": "OrderForm",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+123 456 789",
                    "form": "OrderForm",
                }
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "123 Street",
                    "form": "OrderForm",
                }
            ),
            "address_line_2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "123 Street",
                    "form": "OrderForm",
                }
            ),
            "country": forms.Select(
                attrs={
                    "class": "custom-select",
                    "form": "OrderForm",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "New York",
                    "form": "OrderForm",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "New York",
                    "form": "OrderForm",
                }
            ),
            "zip_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "123",
                    "form": "OrderForm",
                }
            ),
            "price": forms.HiddenInput(
                attrs={
                    "form": "OrderForm",
                }
            ),
        }
