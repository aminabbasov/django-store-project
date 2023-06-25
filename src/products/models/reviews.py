from products.models import Product
from app.models import Timestamped, models
from users.models import User


class Review(Timestamped):
    RATING_CHOICES = [
        (None, 'Rate product'),
        ('1', '1 star'),
        ('2', '2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5', '5 stars'),
    ]

    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    # rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.user.username} - {self.product.name}] - {self.comment}'
