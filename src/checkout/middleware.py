from checkout.basket import Basket


class BasketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response  # noqa: PIE781

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.basket = Basket(request)
