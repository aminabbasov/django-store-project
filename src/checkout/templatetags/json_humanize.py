from typing import Any, TypeAlias

from django import template


json: TypeAlias = dict[str, Any]
register = template.Library()


@register.filter
def json_humanize(stdin: json) -> str:
    stdin = dict(stdin)

    text = []
    for key, value in stdin.items():
        text.append(f"{key} - {value}")

    return "; ".join(text).strip()
