from typing import Any, Callable

from django.http import HttpRequest

from checkout.basket import Basket


class BasketMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response  # noqa: PIE781

    def process_view(self, request: HttpRequest, view_func: Callable, view_args: set, view_kwargs: dict) -> None:
        request.basket = Basket(request)
