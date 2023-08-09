from decimal import Decimal
import pytest

from django.urls import reverse

from products.tests.factories import ProductsReviewFormFactory


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def product(mixer):
    product = mixer.blend("products.Product")
    mixer.blend(
        "products.ProductVariant",
        product=product,
        option={"size": "XL", "color": "black"},
        price=Decimal(100),
        quantity=1,
    )
    return product


def test_shop_view_get_method(client):
    url = reverse("products:shop")
    response = client.get(url)
    assert response.status_code == 200


def test_category_view_get_method(client, category):
    url = reverse("products:category", kwargs={"slug": category.slug})
    response = client.get(url)
    assert response.status_code == 200


def test_detail_view_get_method(client, product):
    url = reverse("products:detail", kwargs={"pk": product.public_id})
    response = client.get(url)
    assert response.status_code == 200


def test_detail_view_no_quatity_post_method(client, product):
    url = reverse("products:detail", kwargs={"pk": product.public_id})
    response = client.post(url, {"quantity": 0, "size": "XL", "color": "black"})
    assert response.status_code == 302


def test_detail_view_valid_post_method(client, product):
    url = reverse("products:detail", kwargs={"pk": product.public_id})
    response = client.post(url, {"quantity": 1, "size": "XL", "color": "black"})
    assert response.status_code == 302


def test_review_view_invalid_form_post_method(client, product):
    url = reverse("products:rate", kwargs={"pk": product.public_id})
    response = client.post(url)
    assert response.status_code == 302


def test_review_view_valid_form_post_method(client, product):
    url = reverse("products:rate", kwargs={"pk": product.public_id})
    data = ProductsReviewFormFactory().data
    response = client.post(url, data=data)
    assert response.status_code == 302
