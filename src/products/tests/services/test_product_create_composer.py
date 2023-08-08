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


def test_with_no_options_product_create_composer(product, price):
    composer = ProductCreateComposer(product, price=price)()
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
def test_with_no_options_product_create_composer(product, price):
    composer = ProductCreateComposer(product, price=price)()
    assert isinstance(composer, dict)
    assert isinstance(composer["product"], Product)
    assert isinstance(composer["options"], ProductOption)
    assert isinstance(composer["variants"], ProductVariant)


def test_price_is_negative_product_create_composer(product, composer_data):
    with pytest.raises(ValueError):
        composer_data["price"] = Decimal(-1)
        ProductCreateComposer(product, **composer_data)()


def test_quantity_is_negative_product_create_composer(product, composer_data):
    with pytest.raises(ValueError):
        composer_data["quantity"] = -1
        ProductCreateComposer(product, **composer_data)()


def test_discount_more_than_100_product_create_composer(product, composer_data):
    with pytest.raises(ValueError):
        composer_data["discount"] = 101
        ProductCreateComposer(product, **composer_data)()


def test_discount_less_than_0_product_create_composer(product, composer_data):
    with pytest.raises(ValueError):
        composer_data["discount"] = -1
        ProductCreateComposer(product, **composer_data)()
