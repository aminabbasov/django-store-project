from django.core.exceptions import ValidationError


class NameValidatorMixin:
    def _name_validator(self, value: str):
        if not value:
            return
        if not value.isalpha():
            raise ValidationError(
                'This field must contain only letters.',
                code='invalid'
            )

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', False)
        self._name_validator(str(value))
        return value
        
    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', False)
        self._name_validator(str(value))
        return value
