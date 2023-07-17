from decimal import Decimal
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models import Min, Max
from django.db.models.functions import Coalesce
from django.db.models import Avg, Value

from app.models import TimestampedModel, models

if __name__ == "__main__":
    from products.models import ProductView


# https://shopify.dev/docs/api/admin-rest/2023-07/resources/product#post-products


# not a class method because i can't write it after attributes definition
def validate_discount(number: int) -> int:
    """Validate and return a discount value within the range 0 to 100."""
    if not (0 <= number <= 100):
        raise ValidationError(
            _(f'The number must be in the range from 0 to 100. Given number is: {number}')
        )

    return number


class ProductQuerySet(models.QuerySet):
    def average_rating(self):
        return self.annotate(avg_rating=Coalesce(Avg('reviews__rating'), Value(0.0)))


class Product(TimestampedModel):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField('products.Category')  # related_name='categories' TODO: look to https://shopify.dev/docs/api/admin-rest/2023-07/resources/collection
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField()
    views = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # vendor = ...  # Example: Apple
    
    objects = ProductQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'uuid': self.public_id})

    @property
    def price_range(self):
        products = ProductView.object.filter(product_id=self.pk)
        min_price = products.get(price=Min())
        max_price = products.get(price=Max())
        return f'{min_price} - {max_price}'

    def __str__(self):
        return self.name


class ProductOption(TimestampedModel):
        product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="options")
        name = models.CharField(max_length=255)
        values = ArrayField(base_field=models.CharField(max_length=255))


class ProductVariant(TimestampedModel):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variants")
    option = models.JSONField()  # Example: {"color": "red", "size": "xl"}
    price = models.DecimalField(max_digits=10, decimal_places=2)  # max: 99,999,999.99 TODO: make JsonField price like this https://shopify.dev/docs/api/admin-rest/2023-07/resources/product-variant#resource-object
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
        name = {'product': self.product.name, **self.option}
        return str(name)
    
    def __str__(self) -> str:
        return self.get_name
