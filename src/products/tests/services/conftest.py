import pytest


@pytest.fixture
def product(mixer):
    return mixer.blend("products.Product")
