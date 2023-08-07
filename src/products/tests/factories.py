from random import randint

import factory

from app.test.factories import BaseFormFactory
from products.forms import ProductsReviewForm


class ProductsReviewFormFactory(BaseFormFactory):
    class Meta:
        model = ProductsReviewForm
        
    rating = randint(1, 5)
    comment = factory.Faker("text")
