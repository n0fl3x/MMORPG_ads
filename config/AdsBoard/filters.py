from django_filters import FilterSet, CharFilter, ChoiceFilter

from .models import CATEGORIES


class AdvFilter(FilterSet):
    category = ChoiceFilter(
        choices=CATEGORIES,
        label='Category',
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title or part of it',
    )

    author = CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
        label="Author's name or part of it",
    )
