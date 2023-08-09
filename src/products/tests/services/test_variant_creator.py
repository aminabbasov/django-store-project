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
    variant_data["price"] = 5
    with pytest.raises(TypeError, match=r"Price must be decimal\. Given type is: .+"):
        ProductVariantCreator(product, **variant_data)()


def test_price_is_negative_variant_creator(product, variant_data):
    variant_data["price"] = Decimal(-1)
    with pytest.raises(ValueError, match="Price can't be less than zero"):
        ProductVariantCreator(product, **variant_data)()


def test_quantity_is_negative_variant_creator(product, variant_data):
    variant_data["quantity"] = -1
    with pytest.raises(ValueError, match="Quantity can't be less than zero"):
        ProductVariantCreator(product, **variant_data)()


def test_discount_less_than_0_variant_creator(product, variant_data):
    variant_data["discount"] = -1
    with pytest.raises(ValueError, match="Discount can't be less than zero"):
        ProductVariantCreator(product, **variant_data)()


def test_discount_more_than_100_variant_creator(product, variant_data):
    variant_data["discount"] = 101
    with pytest.raises(ValueError, match="Discount can't be more than hundred"):
        ProductVariantCreator(product, **variant_data)()
