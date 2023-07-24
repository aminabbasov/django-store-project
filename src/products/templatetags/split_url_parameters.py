from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def split_url_parameters(stdin: str, exclude: str) -> list[list[str, str]]:
    parameters = [parameters for parameters in stdin.split("&")]
    splitted_parameters = list(map(lambda x: x.split("="), parameters))
    filtered_parameters = list(filter(lambda params: params[0] != exclude, splitted_parameters))
    unique_parameters = [list(param) for param in set(tuple(param_list) for param_list in filtered_parameters)]
    without_empty_values = list(filter(lambda x: x[1], unique_parameters))
    return without_empty_values
