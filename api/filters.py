from django import forms
from django_filters import rest_framework as filters
from furniture.models import Category, Furniture

class FurnitureFilter(filters.FilterSet):
    price_from = filters.NumberFilter(
        lookup_expr='gte', 
        field_name='price', 
        label='Цена от'
    )
    price_to = filters.NumberFilter(
        lookup_expr='lte', 
        field_name='price', 
        label='Цена до'
    )
    categories = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(), 
        field_name='category', 
        label='Категории'
    )
    in_stock = filters.BooleanFilter(
        method='filter_in_stock', 
        label='Только в наличии'
    )
    area_from = filters.NumberFilter(
        lookup_expr='gte',
        field_name='area',
        label='Площадь от'
    )
    area_to = filters.NumberFilter(
        lookup_expr='lte',
        field_name='area',
        label='Площадь до'
    )

    sort_by = filters.OrderingFilter(
        fields=(
            ('name', 'Название'),
            ('popularity', 'Популярность'),
            ('area', 'Площадь (м²)'),
            ('price', 'Цена (грн)'),
        ),
        label='Сортировка',
    )

    building_type = filters.ChoiceFilter(
        choices=(
            ('commercial', 'Коммерческие строения'),
            ('residential', 'Дома и жилые строения'),
            ('garden', 'Садовые и хозпостройки'),
        ),
        field_name='building_type',
        label='Тип строения',
        widget=forms.Select, 
    )

    class Meta:
        model = Furniture
        fields = [] 

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(receive_type=Furniture.IN_STOCK)
        return queryset
