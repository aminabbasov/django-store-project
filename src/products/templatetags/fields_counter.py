from django import template

from products.models import SingleProductView


register = template.Library()


@register.simple_tag
def get_price_amount(category=None, price_start=0, price_end=0):
    assert 0 < price_start and 0 < price_end, "Price must be greater than 0"
    assert price_start <= price_end, "Start price must be less than end price"
    
    queryset = SingleProductView.objects.all()
    
    if category:
        queryset = queryset.by_category(category)
    
    if price_start:
        queryset = queryset.filter(max_discounted_price__gte=price_start)
        
    if price_end:
        queryset = queryset.filter(min_discounted_price__lte=price_end)
        
    return queryset.count()


@register.simple_tag
def get_color_amount(category=None, color=None):
    queryset = SingleProductView.objects.all()
    
    if category:
        queryset = queryset.by_category(category)
    
    if color:
        queryset = queryset.by_option(color)
        
    return queryset.count()


@register.simple_tag
def get_size_amount(category=None, size=None):
    queryset = SingleProductView.objects.all()
    
    if category:
        queryset = queryset.by_category(category)
    
    if size:
        queryset = queryset.by_option(size)

    return queryset.count()
