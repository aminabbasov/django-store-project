from random import choice

import factory

from app.test.factories import BaseFormFactory
from checkout.forms import CheckoutOrderCreateForm
from checkout.models import Order


class CheckoutOrderCreateFormFactory(BaseFormFactory):
    class Meta:
        model = CheckoutOrderCreateForm

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    address_line_1 = factory.Faker("street_address")
    address_line_2 = factory.Faker("secondary_address")
    country = choice(Order.COUNTRY.values)
    city = factory.Faker("city")
    state = factory.Faker("state")
    zip_code = factory.Faker("postcode")
    price = factory.Faker("random_number", digits=5, fix_len=False)
