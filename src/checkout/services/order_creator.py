from dataclasses import dataclass
from decimal import Decimal
from functools import singledispatchmethod
from typing import Any, Callable

from app.services import BaseService
from checkout.models import Order
from users.models import User


@dataclass
class OrderCreator(BaseService):
    user: User
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address_line_1: str
    address_line_2: str
    country: str
    city: str
    state: str
    zip_code: str

    price: Decimal | int | float | str = Decimal(0)
    paid: bool = False
    status: str = "Not paid"

    def __post_init__(self) -> None:
        if not isinstance(self.price, Decimal):
            self.price = self._if_not_decimal(self.price)

    def act(self) -> Order:
        return self.create()

    @singledispatchmethod
    def _if_not_decimal(self, price: Any) -> None:
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

    def create(self) -> Order:
        return Order.objects.create(
            user=self.user,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
            address_line_1=self.address_line_1,
            address_line_2=self.address_line_2,
            country=self.country,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            price=self.price,
            paid=self.paid,
            status=self.status,
        )

    def validate_price_is_not_negative(self) -> None:
        if self.price < Decimal(0):
            raise ValueError("Price can't be less than zero")

    def get_validators(self) -> list[Callable]:
        return [
            self.validate_price_is_not_negative,
        ]
