from django.urls import reverse


def test_basket_view_get_method(client):
    url = reverse('checkout:basket')
    response = client.get(url)
    assert response.status_code == 200


def test_basket_view_delete_basket_post_method(client):
    url = reverse('checkout:basket')
    response = client.post(url, {"_method": "delete"})
    assert response.status_code == 302
