from django import template


register = template.Library()


@register.inclusion_tag('inc/_product_card.html')
def product_card(product, template):
    if template == 'index':
        context = {
            'product': product,
            'template': template,
        }
    elif template == 'shop':
        context = {
            'product': product,
            'template': template,
        }
    else:
        raise ValueError('The template (second) argument must only be "index" or "shop".')

    return context
