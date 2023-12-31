from typing import Any

from django.db.models import Q
from django.urls import reverse

from app.models import DefaultModel
from app.models import models
from products.models.categories import CategoryQuerySet
from products.models.products import Product


class ProductViewQuerySet(models.QuerySet):
    def newest(self) -> "ProductViewQuerySet":
        return self.order_by("-product_created")

    def with_discount(self) -> "ProductViewQuerySet":
        return self.filter(discount__gt=0)

    def highest_discount(self) -> "ProductViewQuerySet":
        return self.with_discount().order_by("-discount")

    def newest_discount(self) -> "ProductViewQuerySet":
        return self.with_discount().order_by("-product_created")

    def by_category(self, slug: str) -> "ProductViewQuerySet":
        products = Product.objects.filter(category__slug=slug)
        return self.filter(product_id__in=products)

    def related_products(self, categories: CategoryQuerySet) -> "ProductViewQuerySet":
        products = Product.objects.filter(category__in=categories)
        return self.filter(product_id__in=products)

    def by_options(self, **options: str) -> "ProductViewQuerySet":
        filters = Q()

        for option, value in options.items():
            filters &= Q(**{f"option__{option}__iexact": value})

        return self.filter(filters)


class ProductViewManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(product_available=True).filter(variant_available=True)


class ProductView(DefaultModel):
    """
    This is the PostgreSQL materialized view for
    models Product and ProductVariant.

    Check "products/migrations/0004_create_product_view.py"
    to see raw SQL and trigger funcs for update.
    """

    product_id = models.BigIntegerField()
    variant_id = models.BigIntegerField(
        primary_key=True
    )  # because each model requires exactly one field to have primary_key=True
    public_id = models.UUIDField()

    product_available = models.BooleanField()
    variant_available = models.BooleanField()

    product_created = models.DateTimeField()
    product_modified = models.DateTimeField()
    variant_created = models.DateTimeField()
    variant_modified = models.DateTimeField()

    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField()
    views = models.PositiveIntegerField()

    option = models.JSONField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField()
    quantity = models.PositiveIntegerField()

    objects = ProductViewManager.from_queryset(ProductViewQuerySet)()
    internal = ProductViewQuerySet.as_manager()

    @property
    def images(self) -> Any:
        product = Product.objects.get(pk=self.product_id)
        return product.images

    @property
    def average_rating(self) -> float:
        """Calculate and return the average rating for the product based on reviews."""
        from products.models import Review  # Due to the problem of circular imports

        return Review.objects.filter(product=self.product_id).aggregate(models.Avg("rating"))["rating__avg"] or 0

    @property
    def actual_price(self) -> str:
        """Calculate and return the actual price, considering discounts if applicable."""
        if self.discount:
            return f"${round(self.price - ((self.price * self.discount) / 100), 2)}"
        return f"${self.price}"

    def get_absolute_url(self) -> str:
        return reverse("products:detail", kwargs={"pk": self.public_id})

    class Meta:
        managed = False
        db_table = "products_productview"
