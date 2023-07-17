from django import template


register = template.Library()

@register.filter
def json_humanize(stdin):
    stdin = dict(stdin)
    
    text = []
    for key, value in stdin.items():
        text.append(f"{key} - {value}")
        
    text = "; ".join(text).strip()
    return text
