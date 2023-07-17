from dataclasses import dataclass
from typing import TypeAlias, Annotated, Callable
from decimal import Decimal

from app.services import BaseService
from products.models import Product, ProductVariant


name: TypeAlias = str
value: TypeAlias = str
pk: TypeAlias = int


@dataclass
class ValueRange:
    min: int = 0
    max: int = 100
    

@dataclass
class MinimalValue:
    min: int = 0


@dataclass
class ProductVariantCreator(BaseService):
    product: Product | pk
    option: dict[name, value]  # Example: {"color": "red", "size": "xl"}
    price: Decimal = Decimal(0)
    discount: Annotated[int, ValueRange(0, 100)] = 0
    quantity: Annotated[int, MinimalValue(0)] = 0
    available: bool = False
    
    def __post_init__(self) -> None:
        # Get product by id if necessary
        if isinstance(self.product, int):
            self.product = Product.objects.get(self.product)
    
    def act(self) -> ProductVariant:
        product_variant = self.create()
        return product_variant
    
    def create(self) -> ProductVariant:
        product_variant = ProductVariant.objects.create(
            product=self.product,
            option=self.option,
            price=self.price,
            discount=self.discount,
            quantity=self.quantity,
            available=self.available,
        )
        return product_variant
    
    def validate_price_is_decimal(self) -> None:
        if not isinstance(self.price, Decimal):
            raise AttributeError(f"Price must be decimal. Given type is: {type(self.price)}")
        
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
            self.validate_price_is_decimal,
            self.validate_price_is_not_negative,
            self.validate_quantity_is_not_negative,
            self.validate_discount_is_between_0_and_100,
        ]
