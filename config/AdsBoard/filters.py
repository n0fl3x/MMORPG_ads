from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import RangeWidget, BooleanWidget

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

    date_of_creation = DateFromToRangeFilter(
        label='Range of dates',
        field_name='date_of_creation',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )


class ProfileAdvFilter(FilterSet):
    category = ChoiceFilter(
        choices=CATEGORIES,
        label='Category',
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title or part of it',
    )

    date = DateFromToRangeFilter(
        label='Range of dates',
        field_name='date_of_creation',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )


class ProfileReplyFilter(FilterSet):
    date = DateFromToRangeFilter(
        label='Range of dates',
        field_name='date_of_creation',
        widget=RangeWidget(
            attrs={'type': 'date'},
        ),
    )

    approved = BooleanFilter(
        label='Approved?',
        field_name='is_approved',
        widget=BooleanWidget(),
    )

    rejected = BooleanFilter(
        label='Rejected?',
        field_name='is_rejected',
        widget=BooleanWidget(),
    )
