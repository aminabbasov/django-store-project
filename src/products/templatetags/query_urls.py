from urllib.parse import urlencode

from django import template


register = template.Library()

# https://simpleisbetterthancomplex.com/snippet/2016/08/22/dealing-with-querystring-parameters.html


@register.simple_tag
def query_url(parameters, **kwargs):
    """
    Returns a URL query string with the given parameters and key-value pairs.
    If parameters is not None, any key-value pairs whose keys are not in kwargs will be filtered out.
    """
    url = f"?{urlencode(kwargs)}"

    if parameters:
        querystring = parameters.split("&")
        used_fields = kwargs.keys()
        filtered_querystring = filter(lambda param: param.split("=")[0] not in used_fields, querystring)
        encoded_querystring = "&".join(filtered_querystring)

        if encoded_querystring:
            url += f"&{encoded_querystring}"

    return url
