from django.utils.translation import gettext_lazy as _

from app.models import models
from app.models import TimestampedModel
from products.models import Product
from users.models import User


class Review(TimestampedModel):
    class RATING(models.IntegerChoices):
        __empty__ = _("Rate product")

        ONE_STAR = 1, _("1 star")
        TWO_STARS = 2, _("2 stars")
        THREE_STARS = 3, _("3 stars")
        FOUR_STARS = 4, _("4 stars")
        FIVE_STARS = 5, _("5 stars")

    rating = models.SmallIntegerField(choices=RATING.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(blank=True)

    @property
    def get_date(self):
        return self.modified if self.modified else self.created

    def __str__(self):
        return f"[{self.user.username} - {self.product.name}] - {self.comment}"
