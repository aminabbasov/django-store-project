from dataclasses import dataclass, field
from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest
# from django.contrib.sessions.backends.signed_cookies import SessionStore


@dataclass
class Basket:
    request: HttpRequest
    basket: dict = field(init=False)
    
    def __post_init__(self):
        self.basket = self.request.session.setdefault(settings.BASKET_SESSION_ID, {})
    
    def __str__(self):
        return str(self.basket)
    
    def __iter__(self):
        return iter(self.basket)
    
    def __len__(self):
        return len(self.basket)
    
    def __getitem__(self, key):
        return self.basket[key]
    
    @property
    def get_shipping_price(self):
        return Decimal(10)  # or some cool logic for finding shipping costs
    
    @property
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
    
    @property
    def get_total_price(self):
        return self.get_shipping_price + self.get_subtotal_price
    
    def add(self, variant_id, quantity=1, **options):
        self.basket[variant_id] = {'quantity': quantity,}

        for key, value in options.items():
            self.basket[variant_id][key] = value
        
        #. TODO: find better realisation
        self.basket[variant_id]['total_price'] = (
            str(Decimal(self.basket[variant_id]['quantity']) * Decimal(self.basket[variant_id]['price']))
        )

        self.save()
        
    def remove(self, variant_id):
        if variant_id in self.basket:
            del self.basket[variant_id]

            self.save()

    def save(self):
        self.request.session[settings.BASKET_SESSION_ID] = self.basket
        self.request.session.modified = True

    def clear(self):
        del self.request.session[settings.BASKET_SESSION_ID]
        self.request.session.modified = True

    def keys(self):
        return self.basket.keys()
    
    def values(self):
        return self.basket.values()
    
    def items(self):
        return self.basket.items()