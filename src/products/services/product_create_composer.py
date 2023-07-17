from dataclasses import dataclass
from typing import TypeAlias, Annotated, Any, Callable
from decimal import Decimal
from itertools import product as all_combinations
from enum import Enum
from functools import singledispatchmethod

from django.db import transaction

from app.services import BaseService
from products.models import Product, ProductOption, ProductVariant
from products.services import ProductOptionCreator, ProductVariantCreator


name: TypeAlias = str
value: TypeAlias = str


class ServiceResult(Enum):
    PRODUCT = "product"
    OPTIONS = "options"
    VARIANTS = "variants"


class Default(Enum):
    KEY = "default"
    VALUE = "default"


@dataclass
class ValueRange:
    min: int = 0
    max: int = 100


@dataclass
class MinimalValue:
    min: int = 0


@dataclass
class ProductCreateComposer(BaseService):
    product: Product
    options: dict[name, list[value]] | None = None
    price: Decimal | int | float | str = Decimal(0)
    discount: Annotated[int, ValueRange(0, 100)] = 0
    quantity: Annotated[int, MinimalValue(0)] = 0
    available: bool = False
    
    def __post_init__(self) -> None:
        if not isinstance(self.price, Decimal):
            self.price = self._if_not_decimal(self.price)
    
    def act(self) -> dict[ServiceResult, Any]:
        if self.options is None:
            return self.create_if_no_options()
        
        with transaction.atomic():
            product_options = self.create_option()
            product_variants = self.create_all_combinations()
        
        return \
            {
                ServiceResult.PRODUCT.value: self.product,
                ServiceResult.OPTIONS.value: product_options,
                ServiceResult.VARIANTS.value: product_variants,
            }
    
    @singledispatchmethod
    def _if_not_decimal(self, price):
        raise NotImplementedError("This method is not implemented for the given type")
    
    @_if_not_decimal.register(int)
    def _(self, price: int) -> Decimal:
        return Decimal(price)
    
    @_if_not_decimal.register(float)
    def _(self, price: float) -> Decimal:
        price = str(price)  # because passing float directly to Decimal constructor introduces a rounding error
        return Decimal(price)
    
    @_if_not_decimal.register(str)
    def _(self, price: str) -> Decimal:
        return Decimal(price)
    
    def create_option(self) -> ProductOption:  
        product_options = ProductOptionCreator(
            product=self.product,
            options=self.options,
        )()
        return product_options
    
    def _option_combinations(self) -> list:
        """Generate all possible combinations of product options."""
        result = []
        option_names = list(self.options.keys())

        for combo in all_combinations(*self.options.values()):
            combo_dict = dict(zip(option_names, combo))
            result.append(combo_dict)

        return result

    def create_all_combinations(self) -> list[ProductVariant]:
        """Create all product variants based on option combinations."""
        product_variants = []
        
        for option in self._option_combinations():
            variant = ProductVariantCreator(
                product=self.product,
                option=option,
                price=self.price,
                discount=self.discount,
                quantity=self.quantity,
                available=self.available,
            )()
            product_variants.append(variant)
            
        return product_variants
    
    @transaction.atomic
    def create_if_no_options(self) -> dict[ServiceResult, Any]:
        default_option = ProductOptionCreator(
            product=self.product,
            options={Default.KEY.value: [Default.VALUE.value]},
        )()
        
        default_variant = ProductVariantCreator(
            product=self.product,
            option={Default.KEY.value: Default.VALUE.value},
            price=self.price,
            discount=self.discount,
            quantity=self.quantity,
            available=self.available,
        )()
        
        return \
            {
                ServiceResult.PRODUCT.value: self.product,
                ServiceResult.OPTIONS.value: default_option,
                ServiceResult.VARIANTS.value: default_variant,
            }
    
    def validate_price_is_not_negative(self):
        if self.price < Decimal(0):
            raise ValueError("Price can't be less than zero")
    
    def validate_quantity_is_not_negative(self):
        if self.quantity < 0:
            raise ValueError("Quantity can't be less than zero")
     
    def validate_discount_is_between_0_and_100(self):
        if self.discount < 0:
            raise ValueError("Discount can't be less than zero")
        elif self.discount > 100:
            raise ValueError("Discount can't be more than hundred")
    
    def get_validators(self) -> list[Callable]:
        return [
            self.validate_price_is_not_negative,
            self.validate_quantity_is_not_negative,
            self.validate_discount_is_between_0_and_100,
        ]
