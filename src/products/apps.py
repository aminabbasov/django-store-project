from django.apps import AppConfig
from django.contrib.postgres.fields import ArrayField

from .lookups import ArrayIContains


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        ArrayField.register_lookup(ArrayIContains)
