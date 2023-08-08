from dataclasses import dataclass
from typing import TypeAlias

from django.db import transaction

from app.services import BaseService
from products.models import Product
from products.models import ProductOption


name: TypeAlias = str
values: TypeAlias = list
pk: TypeAlias = int


@dataclass
class ProductOptionCreator(BaseService):
    product: Product | pk
    options: dict[name, values]

    def __post_init__(self) -> None:
        # Get product by id if necessary
        if isinstance(self.product, int):
            self.product = Product.objects.get(pk=self.product)

    def act(self) -> ProductOption | list[ProductOption]:
        product_options = self.create()
        return product_options

    @transaction.atomic
    def create(self) -> ProductOption | list[ProductOption]:
        product_options = []
        for key, value in self.options.items():
            product_options.append(
                ProductOption.objects.create(
                    product=self.product,
                    name=key,
                    values=value,
                )
            )

        if len(product_options) == 1:
            return product_options[0]

        return product_options
