from django import template

register = template.Library()


@register.filter
def listing(number: int) -> list:
    """Simple filter to use in HTML-templates for pagination."""

    pagination_list = []
    for n in range(number):
        pagination_list.append(n + 1)
    return pagination_list
