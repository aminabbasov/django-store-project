from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal
from typing import Any, ItemsView, Iterator, KeysView, ValuesView

from django.conf import settings
from django.http import HttpRequest


@dataclass
class Basket:
    request: HttpRequest
    basket: dict = field(init=False)

    def __post_init__(self) -> None:
        self.basket = self.request.session.setdefault(settings.BASKET_SESSION_ID, {})

    def __str__(self) -> str:
        return str(self.basket)

    def __iter__(self) -> Iterator:
        return iter(self.basket)

    def __len__(self) -> int:
        return len(self.basket)

    def __getitem__(self, key: str) -> Any:
        return self.basket[key]

    @property
    def get_shipping_price(self) -> Decimal:
        return Decimal(10)  # or some cool logic for finding shipping costs

    @property
    def get_subtotal_price(self) -> Decimal:
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.basket.values())

    @property
    def get_total_price(self) -> Decimal:
        return self.get_shipping_price + self.get_subtotal_price

    def add(self, variant_id: int, quantity: int = 1, **options) -> None:
        self.basket[variant_id] = {
            "quantity": quantity,
        }

        for key, value in options.items():
            self.basket[variant_id][key] = value

        self.basket[variant_id]["total_price"] = str(
            Decimal(self.basket[variant_id]["quantity"]) * Decimal(self.basket[variant_id]["price"])
        )

        self.save()

    def remove(self, variant_id: int) -> None:
        if variant_id in self.basket:
            del self.basket[variant_id]

            self.save()

    def save(self) -> None:
        self.request.session[settings.BASKET_SESSION_ID] = self.basket
        self.request.session.modified = True

    def clear(self) -> None:
        del self.request.session[settings.BASKET_SESSION_ID]
        self.request.session.modified = True

    def keys(self) -> KeysView:
        return self.basket.keys()

    def values(self) -> ValuesView:
        return self.basket.values()

    def items(self) -> ItemsView:
        return self.basket.items()
