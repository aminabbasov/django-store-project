import pytest


@pytest.fixture
def category(mixer):
    return mixer.blend("products.Category", name="shirts")
