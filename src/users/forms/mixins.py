from django.core.exceptions import ValidationError


class NameValidatorMixin:
    def _name_validator(self, value: str, field_name: str):
        if not value:
            return
        if not value.isalpha():
            raise ValidationError(
                f'Field "{field_name}" must contain only letters.',
                code='invalid'
            )

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', False)
        self._name_validator(str(value), "first name")
        return value
        
    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', False)
        self._name_validator(str(value), "last name")
        return value
