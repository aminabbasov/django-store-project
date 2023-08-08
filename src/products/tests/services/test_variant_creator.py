from decimal import Decimal
import pytest

from products.models import ProductVariant
from products.services import ProductVariantCreator


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def variant_data():
    return {"option": {"default": "default"}}


def test_variant_creator(product, variant_data):
    variant = ProductVariantCreator(product, **variant_data)()
    assert isinstance(variant, ProductVariant)


def test_product_is_pk_variant_creator(product, variant_data):
    variant = ProductVariantCreator(product.id, **variant_data)()
    assert isinstance(variant, ProductVariant)


def test_price_is_not_decimal_variant_creator(product, variant_data):
    with pytest.raises(AttributeError):
        variant_data["price"] = 5
        ProductVariantCreator(product, **variant_data)()


def test_price_is_negative_variant_creator(product, variant_data):
    with pytest.raises(ValueError):
        variant_data["price"] = Decimal(-1)
        ProductVariantCreator(product, **variant_data)()


def test_quantity_is_negative_variant_creator(product, variant_data):
    with pytest.raises(ValueError):
        variant_data["quantity"] = -1
        ProductVariantCreator(product, **variant_data)()


def test_discount_more_than_100_variant_creator(product, variant_data):
    with pytest.raises(ValueError):
        variant_data["discount"] = 101
        ProductVariantCreator(product, **variant_data)()


def test_discount_less_than_0_variant_creator(product, variant_data):
    with pytest.raises(ValueError):
        variant_data["discount"] = -1
        ProductVariantCreator(product, **variant_data)()
