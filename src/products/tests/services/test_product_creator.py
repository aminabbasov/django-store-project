import pytest

from products.services import ProductCreator
from products.models import Product


@pytest.fixture
def product_data(category):
    return {
        "name": "Test",
        "category": category,
    }


@pytest.mark.django_db
def test_product_creator(product_data):
    product = ProductCreator(**product_data)()
    assert isinstance(product, Product)
