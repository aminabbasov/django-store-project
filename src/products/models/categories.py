from typing import Any

from django.db.models import Case
from django.db.models import Count
from django.db.models import IntegerField
from django.db.models import Value
from django.db.models import When
from django.urls import reverse
from django.utils.text import slugify

from app.models import models
from app.models import TimestampedModel


class CategoryQuerySet(models.QuerySet):
    def manual_order(self, categories: list[str]) -> "CategoryQuerySet":
        """Order of the categories will follow the order in the list."""
        return self.filter(name__in=categories).order_by(
            Case(
                *[When(name=name, then=Value(value)) for value, name in enumerate(categories, 1)],
                output_field=IntegerField(),
            )
        )

    def annotate_product_count(self) -> "CategoryQuerySet":
        return self.annotate(product_amount=Count("product"))


class Category(TimestampedModel):
    # because models.TextChoices doesn't support nesting
    CATEGORY_CHOICES = [
        (None, "Select category"),
        (
            "Dresses",
            (
                ("man", "Men's Dresses"),
                ("woman", "Women's Dresses"),
                ("baby", "Baby's Dresses"),
            ),
        ),
        ("shirts", "Shirts"),
        ("jeans", "Jeans"),
        ("swimwear", "Swimwear"),
        ("sleepwear", "Sleepwear"),
        ("sportswear", "Sportswear"),
        ("jumpsuits", "Jumpsuits"),
        ("blazers", "Blazers"),
        ("jackets", "Jackets"),
        ("shoes", "Shoes"),
    ]

    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES, db_index=True, unique=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="category", null=True, blank=True)
    slug = models.SlugField(unique=True)

    objects = CategoryQuerySet.as_manager()

    def get_absolute_url(self) -> str:
        return reverse("products:category", kwargs={"slug": self.slug})

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        storage, path = self.image.storage, self.image.path
        super().delete(*args, **kwargs)
        storage.delete(path)

    @property
    def get_image_url(self) -> str:
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return ""

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
