from django import template
from django.template import TemplateSyntaxError


register = template.Library()


@register.inclusion_tag("inc/_product_card.html")
def product_card(product, template):
    match template:
        case "index":
            context = {
                "product": product,
                "template": template,
            }
        case "shop":
            context = {
                "product": product,
                "template": template,
            }
        case _:
            raise TemplateSyntaxError('The template (second) argument must only be "index" or "shop".')

    return context
