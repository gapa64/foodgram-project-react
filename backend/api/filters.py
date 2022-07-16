from django_filters.rest_framework import filters, FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class NameFilter(SearchFilter):
    search_param = 'name'


class RecipeFilterSet(FilterSet):

    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = [
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'tags'
        ]

    def filter_is_favorited(self, queryset, name, value):
        if value is not None:
            return queryset.filter(favorited_users__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(buyers__user=self.request.user)
        return queryset
