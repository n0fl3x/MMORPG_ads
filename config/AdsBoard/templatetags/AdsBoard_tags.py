from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Custom tag to use in HTML-templates
    which takes some kwargs in template and add them to QueryDict."""

    context_copy = context['request'].GET.copy()
    for a, b in kwargs.items():
        context_copy[a] = b
    return context_copy.urlencode()
