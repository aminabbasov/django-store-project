from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        
    def __str__(self):
        return str(self.cart)
        
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]['pk'] = str(product.id)

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    @property
    def get_shipping_price(self):
        return Decimal(10)  # or some cool logic for finding shipping costs
    
    @property
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    @property
    def get_total_price(self):
        return self.get_shipping_price + sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def add(self, product, size, color, quantity=1, update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'price': str(product.actual_price),
                'size': str(size),
                'color': str(color),
                'quantity': 0,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()
        
    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    def save(self): 
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
