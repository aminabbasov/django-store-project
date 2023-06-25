from django.utils.deprecation import MiddlewareMixin
from checkout.cart import Cart

 
class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.cart = Cart(request)
