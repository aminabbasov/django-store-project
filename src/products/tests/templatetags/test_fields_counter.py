from decimal import Decimal
import pytest

from products.templatetags.fields_counter import get_color_amount
from products.templatetags.fields_counter import get_price_amount
from products.templatetags.fields_counter import get_size_amount


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def categories(mixer):
    return mixer.cycle(2).blend("products.Category", name=(c for c in ("shirts", "jeans")))


@pytest.fixture
def products(mixer, categories):
    return mixer.cycle(2).blend("products.Product", category=(c for c in categories))


@pytest.fixture(autouse=True)
def product_options(mixer, products):
    for product in products:
        mixer.cycle(2).blend(
            "products.ProductOption",
            product=product,
            name=(n for n in ["color", "size"]),
            values=(v for v in [["black", "white"], ["S", "XL"]]),
        )


@pytest.fixture(autouse=True)
def products_variants(mixer, products):
    options = (
        {"color": "black", "size": "S"},
        {"color": "black", "size": "XL"},
        {"color": "white", "size": "S"},
        {"color": "white", "size": "XL"},
    )

    product_1_prices = (
        Decimal("10"),
        Decimal("101"),
        Decimal("199.99"),
        Decimal("500"),
    )
    product_2_prices = (
        Decimal("200"),
        Decimal("300"),
        Decimal("400"),
        Decimal("500"),
    )

    variants = []

    for product, prices in zip(products, [product_1_prices, product_2_prices]):
        variant = mixer.cycle(4).blend(
            "products.ProductVariant",
            product=product,
            option=(d for d in options),
            price=(p for p in prices),
        )
        variants = variants + variant

    return variants


class TestGetPriceAmount:
    def test_full_range_without_category(self):
        result = get_price_amount(price_start=1, price_end=501)
        assert result == 2

    def test_part_of_range_without_category(self):
        result = get_price_amount(price_start=1, price_end=199)
        assert result == 1

    def test_full_range_with_category(self):
        result = get_price_amount(category="jeans", price_start=1, price_end=500)
        assert result == 1


class TestGetColorAmount:
    def test_color_without_category(self):
        result = get_color_amount(color="white")
        assert result == 2

    def test_color_with_category(self):
        result = get_color_amount(category="shirts", color="black")
        assert result == 1


class TestGetSizeAmount:
    def test_size_without_category(self):
        result = get_size_amount(size="XL")
        assert result == 2

    def test_size_with_category(self):
        result = get_size_amount(category="shirts", size="S")
        assert result == 1
