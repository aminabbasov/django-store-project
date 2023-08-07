import pytest

from products.services import ProductOptionCreator
from products.models import ProductOption


pytestmark = [pytest.mark.django_db]

@pytest.fixture
def multiple_option_data():
    return {
        "color": ["black", "white"],
        "size": ["S", "XL"],
    }


@pytest.fixture
def single_option_data():
    return {
        "default": ["default"],
    }


def test_multiple_option_creator(product, multiple_option_data):
    option = ProductOptionCreator(product, multiple_option_data)()
    assert isinstance(option[0], ProductOption)


def test_single_option_creator(product, single_option_data):
    option = ProductOptionCreator(product, single_option_data)()
    assert isinstance(option, ProductOption)


def test_product_is_pk_option_creator(product, single_option_data):
    option = ProductOptionCreator(product.id, single_option_data)()
    assert isinstance(option, ProductOption)
