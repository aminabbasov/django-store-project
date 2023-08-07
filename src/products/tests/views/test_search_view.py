import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_search_view_get_method(client):
    url = reverse('products:search') + "?q=test"
    response = client.get(url)
    assert response.status_code == 200
