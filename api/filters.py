from django_filters import rest_framework as filters
from furniture.models import Category, Furniture
from django.db import models

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

    class Meta:
        model = Furniture
        fields = [] 
        filter_overrides = {
            models.ImageField: {  
                'filter_class': filters.CharFilter,  
            },
        }

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(receive_type=Furniture.IN_STOCK)
        return queryset
