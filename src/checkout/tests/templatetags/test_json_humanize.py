from checkout.templatetags import json_humanize


def test_json_humanize():
    data = {"foo1": "bar1", "foo2": "bar2"}
    expected = "foo1 - bar1; foo2 - bar2"
    result = json_humanize(data)
    assert result == expected
