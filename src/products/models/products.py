from decimal import Decimal
import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.models import models
from app.models import TimestampedModel


# https://shopify.dev/docs/api/admin-rest/2023-07/resources/product#post-products


# not a class method because i can't write it after attributes definition
def validate_discount(number: int) -> int:
    """Validate and return a discount value within the range 0 to 100."""
    if not (0 <= number <= 100):
        raise ValidationError(_(f"The number must be in the range from 0 to 100. Given number is: {number}"))

    return number


class ProductQuerySet(models.QuerySet):
    def average_rating(self):
        return self.annotate(avg_rating=Coalesce(Avg("reviews__rating"), Value(0.0)))


class Product(TimestampedModel):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(
        "products.Category"
    )  # related_name='categories' TODO: look to https://shopify.dev/docs/api/admin-rest/2023-07/resources/collection
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField()
    views = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = ProductQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.public_id})

    @property
    def price_range(self):
        from products.models import SingleProductView  # due to circular import exception

        product = SingleProductView.objects.get(public_id=self.public_id)
        min_price = product.min_discounted_price
        max_price = product.max_discounted_price

        if min_price == max_price:
            return f"${min_price}"

        return f"${min_price} - ${max_price}"

    def __str__(self):
        return self.name


class ProductOption(TimestampedModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=255)
    values = ArrayField(base_field=models.CharField(max_length=255))


class ProductVariant(TimestampedModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variants")
    option = models.JSONField()  # Example: {"color": "black", "size": "XL"}
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # max: 99,999,999.99 TODO: make JsonField price like this https://shopify.dev/docs/api/admin-rest/2023-07/resources/product-variant#resource-object
    discount = models.IntegerField(default=0, validators=[validate_discount])
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    @property
    def actual_price(self) -> Decimal:
        """Calculate and return the actual price, considering discounts if applicable."""
        if self.discount:
            return round(self.price - ((self.price * self.discount) / 100), 2)
        return self.price

    @property
    def get_name(self) -> str:  # names may conflict, they are not unique TODO: fix it
        name = {"product": self.product.name, **self.option}
        return str(name)

    def __str__(self) -> str:
        return self.get_name
