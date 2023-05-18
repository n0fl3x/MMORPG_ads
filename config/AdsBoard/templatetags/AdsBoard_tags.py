from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Custom tag to use in HTML-templates
    which takes some kwargs in template and add them to QueryDict."""

    context_copy = context['request'].GET.copy()
    for key, value in kwargs.items():
        context_copy[key] = value
    return context_copy.urlencode()
