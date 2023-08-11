from django import template

from products.models import SingleProductView


register = template.Library()


@register.simple_tag
def get_price_amount(category: str | None = None, price_start: int | float = 0, price_end: int | float = 0) -> int:
    queryset = SingleProductView.objects.all()

    if category:
        queryset = queryset.by_category(category)

    if price_start:
        queryset = queryset.filter(max_discounted_price__gte=price_start)

    if price_end:
        queryset = queryset.filter(min_discounted_price__lte=price_end)

    return queryset.count()


@register.simple_tag
def get_color_amount(category: str | None = None, color: str | None = None) -> int:
    queryset = SingleProductView.objects.all()

    if category:
        queryset = queryset.by_category(category)

    if color:
        queryset = queryset.by_option(color)

    return queryset.count()


@register.simple_tag
def get_size_amount(category: str | None = None, size: str | None = None) -> int:
    queryset = SingleProductView.objects.all()

    if category:
        queryset = queryset.by_category(category)

    if size:
        queryset = queryset.by_option(size)

    return queryset.count()
