import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_index_view_get_method(client):
    url = reverse('products:index')
    response = client.get(url)
    assert response.status_code == 200
