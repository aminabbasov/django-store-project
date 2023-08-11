from decimal import Decimal
import pytest

from products.models import Product
from products.models import ProductOption
from products.models import ProductVariant
from products.services import ProductCreateComposer


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def composer_data():
    return {"options": {"default": ["default"]}}


@pytest.fixture
def multiple_composer_data():
    return {
        "options": {
            "color": ["black", "white"],
            "size": ["S", "XL"],
        }
    }


def test_single_option_product_create_composer(product, composer_data):
    composer = ProductCreateComposer(product, **composer_data)()
    assert isinstance(composer, dict)
    assert isinstance(composer["product"], Product)
    assert isinstance(composer["options"], ProductOption)
    assert isinstance(composer["variants"], ProductVariant)


def test_multiple_options_product_create_composer(product, multiple_composer_data):
    composer = ProductCreateComposer(product, **multiple_composer_data)()
    assert isinstance(composer, dict)
    assert isinstance(composer["product"], Product)
    assert isinstance(composer["options"][0], ProductOption)
    assert isinstance(composer["variants"][0], ProductVariant)


def test_with_no_options_product_create_composer(product):
    composer = ProductCreateComposer(product)()
    assert isinstance(composer, dict)
    assert isinstance(composer["product"], Product)
    assert isinstance(composer["options"], ProductOption)
    assert isinstance(composer["variants"], ProductVariant)


@pytest.mark.parametrize(
    "price",
    [
        Decimal(10),
        int(10),
        float(10),
        str(10),
    ],
)
def test_prices_product_create_composer(product, price):
    composer = ProductCreateComposer(product, price=price)()
    assert isinstance(composer, dict)
    assert isinstance(composer["product"], Product)
    assert isinstance(composer["options"], ProductOption)
    assert isinstance(composer["variants"], ProductVariant)


def test_price_is_negative_product_create_composer(product, composer_data):
    composer_data["price"] = Decimal(-1)
    with pytest.raises(ValueError, match="Price can't be less than zero"):
        ProductCreateComposer(product, **composer_data)()


def test_quantity_is_negative_product_create_composer(product, composer_data):
    composer_data["quantity"] = -1
    with pytest.raises(ValueError, match="Quantity can't be less than zero"):
        ProductCreateComposer(product, **composer_data)()


def test_discount_less_than_0_product_create_composer(product, composer_data):
    composer_data["discount"] = -1
    with pytest.raises(ValueError, match="Discount can't be less than zero"):
        ProductCreateComposer(product, **composer_data)()


def test_discount_more_than_100_product_create_composer(product, composer_data):
    composer_data["discount"] = 101
    with pytest.raises(ValueError, match="Discount can't be more than hundred"):
        ProductCreateComposer(product, **composer_data)()
