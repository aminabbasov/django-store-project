from django import template

from urllib.parse import urlencode


register = template.Library()

# https://simpleisbetterthancomplex.com/snippet/2016/08/22/dealing-with-querystring-parameters.html

# @register.simple_tag
# def relative_url(value, field_name, urlencode=None):
#     url = '?{}={}'.format(field_name, value)

#     if urlencode:
#         querystring = urlencode.split('&')
#         filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
#         encoded_querystring = '&'.join(filtered_querystring)
#         url = '{}&{}'.format(url, encoded_querystring)

#     return url


# @register.simple_tag
# def query_url(urlencode=None, **parameters):
#     """
#     Returns a URL query string with the given parameters and key-value pairs.
#     If parameters is not None, any key-value pairs whose keys are not in kwargs will be filtered out.
#     """
#     url = '?' + '&'.join([f'{field}={value}' for field, value in parameters.items()])

#     if urlencode:
#         querystring = urlencode.split('&')
#         used_fields = parameters.keys()
#         filtered_querystring = filter(lambda p: p.split('=')[0] not in used_fields, querystring)
#         encoded_querystring = '&'.join(filtered_querystring)

#         url += f'&{encoded_querystring}'

#     return url


@register.simple_tag
def query_url(parameters, **kwargs):
    """
    Returns a URL query string with the given parameters and key-value pairs.
    If parameters is not None, any key-value pairs whose keys are not in kwargs will be filtered out.
    """
    url = f'?{urlencode(kwargs)}'

    if parameters:
        querystring = parameters.split('&')
        used_fields = kwargs.keys()
        filtered_querystring = filter(lambda param: param.split('=')[0] not in used_fields, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        
        if encoded_querystring:
            url += f'&{encoded_querystring}'

    return url


# @register.simple_tag
# def query_url(parameters, **kwargs):
#     """
#     Returns a URL query string with the given parameters and key-value pairs.
#     If parameters is not None, any key-value pairs whose keys are not in kwargs will be filtered out.
#     """
#     query_dict = kwargs.copy()
    
#     if parameters:
#         allowed_fields = set(parameters.split('&'))
#         query_dict = {key: value for key, value in kwargs.items() if key in allowed_fields}

#     url = f'?{urlencode(query_dict)}'
#     return url
