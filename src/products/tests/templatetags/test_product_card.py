import pytest

from products.templatetags.product_cards import product_card


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def product(mixer):
    return mixer.blend("products.Product")


@pytest.mark.parametrize(
    "model, template",
    [
        ("product", "index"),
        ("product", "shop"),
    ],
)
def test_valid_product_card(model, template, request):
    fixture_value = request.getfixturevalue(model)
    result = product_card(product=fixture_value, template=template)
    assert result == {"product": fixture_value, "template": template}


def test_invalid_product_card(product):
    with pytest.raises(ValueError):
        product_card(product=product, template="INVALID VALUE")
