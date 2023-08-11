from dataclasses import dataclass
from decimal import Decimal
from functools import singledispatchmethod
from typing import Annotated, Any, Callable, TypeAlias

from app.services import BaseService
from checkout.models import Order
from checkout.models import OrderItem
from products.models import Product


name: TypeAlias = str
value: TypeAlias = str


@dataclass
class MinimalValue:
    min: int = 1


@dataclass
class OrderItemCreator(BaseService):
    order: Order
    product: Product
    option: dict[name, value]  # Example: {"color": "red", "size": "xl"}
    price: Decimal | int | float | str = Decimal(0)
    quantity: Annotated[int, MinimalValue(1)] = 1

    def __post_init__(self) -> None:
        if not isinstance(self.price, Decimal):
            self.price = self._if_not_decimal(self.price)

    def act(self) -> OrderItem:
        return self.create()

    @singledispatchmethod
    def _if_not_decimal(self, price: Any) -> None:
        raise NotImplementedError(f"This method is not implemented for the given type. Type is {type(price)}.")

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

    def create(self) -> OrderItem:
        return OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.price,
            quantity=self.quantity,
            option=self.option,
        )

    def validate_price_is_not_negative(self) -> None:
        if self.price < Decimal(0):
            raise ValueError("Price can't be less than zero")

    def validate_quantity_is_not_negative(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity can't be less than zero")

    def get_validators(self) -> list[Callable]:
        return [
            self.validate_price_is_not_negative,
            self.validate_quantity_is_not_negative,
        ]
