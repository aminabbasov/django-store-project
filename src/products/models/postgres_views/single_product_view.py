from django.urls import reverse
from django.db.models import Case, When, Value, BigIntegerField

from app.models import models, DefaultModel
from ..products import Product, ProductOption


class SingleProductViewQuerySet(models.QuerySet):
    def newest(self):
        return self.order_by('-created')
    
    def with_discount(self):
        return self.filter(max_discount__gt=0)
    
    def highest_discount(self):
        return self.with_discount().order_by('-max_discount')
    
    def newest_discount(self):
        return self.with_discount().order_by('-created')
    
    def by_category(self, slug: str):
        products = Product.objects.filter(category__slug=slug)  # XXX .values_list("id")
        return self.filter(product_id__in=products)
    
    def related_products(self, categories, exclude_model=None):
        products = Product.objects.filter(category__in=categories)
        
        if exclude_model:
            products = products.exclude(public_id=exclude_model.public_id)
        
        return self.filter(product_id__in=products)
    
    def by_option(self, value: str):
        product_option = ProductOption.objects.filter(
            values__icontains=value  # icontains is a custom lookup
        )
        product_ids = [item.product.id for item in product_option]
        return self.filter(product_id__in=product_ids)
    
    def manual_order(self, ids: list[int]):
        """Order of the products will follow the order in the list."""
        ordered_products = self.filter(product_id__in=ids).order_by(
            Case(
                *[When(product_id=pk, then=Value(value)) for value, pk in enumerate(ids, 1)],
                output_field=BigIntegerField(),
            )
        )
        return ordered_products


class SingleProductView(DefaultModel):
    """
    !IMPORTANT: It contains only available products.
    
    This is the PostgreSQL materialized view for model Product.

    Check "products/migrations/0006_create_single_product_view.py"
    to see raw SQL and trigger funcs for update.
    """
    product_id = models.BigIntegerField(primary_key=True)  # because each model requires exactly one field to have primary_key=True
    public_id = models.UUIDField()
    available = models.BooleanField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField()
    views = models.PositiveIntegerField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_discount = models.IntegerField()
    max_discount = models.IntegerField()
    quantity = models.PositiveIntegerField()

    objects = SingleProductViewQuerySet.as_manager()

    @property
    def images(self):
        product = Product.objects.get(pk=self.product_id)  #X TODO: think about better realization
        return product.images
    
    @property
    def reviews(self):
        product = Product.objects.get(pk=self.product_id)  #X TODO: think about better realization
        return product.reviews
    
    @property
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.public_id})
    
    @property
    def has_discount(self):
        if self.max_discount:
            return True
        return False
    
    @property
    def price_range(self):
        if self.min_price != self.max_price:
            return f"${self.min_price} - ${self.max_price}"
        return f'${self.max_price}'
    
    @property
    def discounted_price_range(self):
        if self.min_discounted_price != self.max_discounted_price:
            return f"${self.min_discounted_price} - ${self.max_discounted_price}"
        return f'${self.max_discounted_price}'
    
    def average_rating(self) -> int | float:
        """Calculate and return the average rating for the product based on reviews."""
        from products.models import Review  # Due to the problem of circular imports

        return Review.objects.filter(product=self.product_id).aggregate(models.Avg("rating"))["rating__avg"] or 0
    
    class Meta:
        managed = False
        db_table = "products_singleproductview"
