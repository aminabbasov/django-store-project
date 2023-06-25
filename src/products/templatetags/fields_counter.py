from django import template

from products.models import Product


register = template.Library()


@register.simple_tag
def get_price_amount(category=None, price_start=0, price_end=0):
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    if price_start:
        queryset = queryset.filter(price__gte=price_start)
        
    if price_end:
        queryset = queryset.filter(price__lte=price_end)
        
    return queryset.count()


@register.simple_tag
def get_color_amount(category=None, color=None):
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    if color:
        queryset = queryset.filter(color=color)
        
    return queryset.count()


@register.simple_tag
def get_size_amount(category=None, size=None):
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category__slug=category)
    
    if size:
        queryset = queryset.filter(size=size)

    return queryset.count()
