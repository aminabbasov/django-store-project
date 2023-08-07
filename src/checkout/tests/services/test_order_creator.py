from decimal import Decimal

import pytest

from checkout.models import Order
from checkout.services import OrderCreator
from checkout.tests.factories import CheckoutOrderCreateFormFactory


pytestmark = [pytest.mark.django_db]

@pytest.fixture
def order_data():
    return CheckoutOrderCreateFormFactory().data


@pytest.mark.parametrize(
    "price",
    [
        Decimal(10),
        int(10),
        float(10),
        str(10),
    ]
)
def test_order_creator(user, order_data, price):
    order_data["price"] = price
    order = OrderCreator(user, **order_data)()
    assert isinstance(order, Order)


def test_price_less_than_0_order_creator(user, order_data):
    with pytest.raises(ValueError):
        order_data["price"] = -1
        OrderCreator(user, **order_data)()
