import pytest

from products.templatetags.query_urls import query_url


@pytest.fixture
def url():
    return "first_param=1&second_param=2"


def test_query_url(url):
    result = query_url(url, third_param=3)
    assert result == "?third_param=3&first_param=1&second_param=2"
