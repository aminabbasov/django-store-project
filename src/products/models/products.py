from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from app.models import Timestamped, models


def validate_discount(number: int) -> int:
        if not 0 <= number <= 100:
            raise ValidationError(
                _(f'The number must be in the range from 0 to 100. Given number is: {number}')
            )

        return number


class Product(Timestamped):
    
    class SIZES(models.TextChoices):        
        __empty__ = _('Select size')

        XS = 'XS', 'XS'
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
       
    class COLORS(models.TextChoices): 
        __empty__ = _('Select color')

        BLACK = 'black', _('Black')
        WHITE = 'white', _('White')
        RED = 'red', _('Red')
        BLUE = 'blue', _('Blue')
        GREEN = 'green', _('Green')
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # max: 99999.99
    discount = models.IntegerField(default=0, validators=[validate_discount])
    short_description = models.CharField(max_length=255)
    size = models.CharField(max_length=30, choices=SIZES.choices)
    color = models.CharField(max_length=30, choices=COLORS.choices)
    description = models.TextField()
    information = models.TextField()
    views = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField('Category')  # related_name='categories'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    @property
    def average_rating(self) -> float:
        from products.models import Review  # Due to the problem of circular imports

        return Review.objects.filter(product=self).aggregate(models.Avg("rating"))["rating__avg"] or 0
    
    @property
    def actual_price(self):
        if self.discount:
            return round(self.price - ((self.price * self.discount) / 100), 2)
        return self.price

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
    
    # class Meta:
        # ordering = ['-date']
