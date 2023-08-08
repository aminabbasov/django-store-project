import pytest

from products.templatetags.split_url_parameters import split_url_parameters


@pytest.fixture
def parameters():
    return "first_param=1&second_param=2&exclude_param=3"


def test_split_url_parameters(parameters):
    result = split_url_parameters(parameters, "exclude_param")
    expected_output_1 = [["first_param", "1"], ["second_param", "2"]]
    expected_output_2 = [["second_param", "2"], ["first_param", "1"]]
    assert result == expected_output_1 or result == expected_output_2
