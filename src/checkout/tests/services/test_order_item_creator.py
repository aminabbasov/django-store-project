from decimal import Decimal
import pytest

from checkout.models import OrderItem
from checkout.services import OrderItemCreator


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order(mixer):
    return mixer.blend("checkout.Order")


@pytest.fixture
def product(mixer):
    return mixer.blend("products.Product")


@pytest.fixture
def options():
    return {"option": {"default": "default"}}


@pytest.mark.parametrize(
    "price",
    [
        Decimal(10),
        int(10),
        float(10),
        str(10),
    ],
)
def test_order_item_creator(order, product, options, price):
    options["price"] = price
    order_item = OrderItemCreator(order, product, **options)()
    assert isinstance(order_item, OrderItem)


def test_price_less_than_0_order_creator(order, product, options):
    options["price"] = -1
    with pytest.raises(ValueError, match="Price can't be less than zero"):
        OrderItemCreator(order, product, **options)()


def test_quantity_less_than_0_order_creator(order, product, options):
    options["quantity"] = -1
    with pytest.raises(ValueError, match="Quantity can't be less than zero"):
        OrderItemCreator(order, product, **options)()
