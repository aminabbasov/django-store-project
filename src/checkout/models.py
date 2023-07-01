from app.models import models, TimestampedModel

from users.models import User
from products.models import Product


class Order(TimestampedModel):
    COUNTRY_CHOICES = [
        ('us', 'United States'),
        ('germany', 'Germany'),
        ('turkey', 'Turkey'),
        ('uae', 'United Arab Emirates'),                 #! СДЕЛАТЬ ДВОЙНЫЕ КОДЫ СТРАН КАК У США
        ('thailand', 'Thailand'),
        ('japan', 'Japan'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('In transit', 'In transit'),
        ('Shipped', 'Shipped'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='address')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(default='us', max_length=30, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    paid = models.BooleanField(default=False)
    status = models.CharField(default='Pending', max_length=30, choices=STATUS_CHOICES)
    
    def __str__(self):
        return str(self.id)

    @property
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


SIZE_CHOICES = [
    (None, 'Select size'),

    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
]

COLOR_CHOICES = [
    (None, 'Select color'),
    
    ('black', 'Black'),
    ('white', 'White'),
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
]

class OrderItem(TimestampedModel):    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='ordered_items')  #! ordered_item
    price = models.DecimalField(max_digits=7, decimal_places=2)
    size = models.CharField(max_length=30, choices=SIZE_CHOICES)
    color = models.CharField(max_length=30, choices=COLOR_CHOICES)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
