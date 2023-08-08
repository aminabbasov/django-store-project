from django.utils.translation import gettext_lazy as _

from app.models import models
from app.models import TimestampedModel
from products.models import Product
from users.models import User


class OrderQuerySet(models.QuerySet):
    def filter_by_user(self, user):
        filtered_orders = Order.objects.annotate().filter(user=user)
        return filtered_orders


class Order(TimestampedModel):
    class COUNTRY(models.TextChoices):
        US = "US", _("United States")
        DE = "DE", _("Germany")
        TR = "TR", _("Turkey")
        AE = "AE", _("United Arab Emirates")
        TH = "TH", _("Thailand")
        JP = "JP", _("Japan")

    class STATUS(models.TextChoices):
        NOT_PAID = "Not paid", _("Not paid")
        PENDING = "Pending", _("Pending")
        APPROVED = "Approved", _("Approved")
        IN_TRANSIT = "In transit", _("In transit")
        SHIPPED = "Shipped", _("Shipped")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="address")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(default=COUNTRY.US, max_length=255, choices=COUNTRY.choices)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=255, blank=True)

    price = models.DecimalField(max_digits=7, decimal_places=2)
    paid = models.BooleanField(default=False)
    status = models.CharField(default=STATUS.NOT_PAID, max_length=255, choices=STATUS.choices)

    objects = OrderQuerySet.as_manager()

    def __str__(self):
        return str(self.id)

    @property
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="ordered_items")
    option = models.JSONField()  # Example: {"color": "red", "size": "xl"}
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
