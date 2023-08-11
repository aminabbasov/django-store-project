from typing import Literal

from django.http import HttpRequest

from checkout.basket import Basket


def basket(request: HttpRequest) -> dict[Literal["basket"], Basket]:
    return {"basket": Basket(request)}
