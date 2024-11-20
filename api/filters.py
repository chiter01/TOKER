from django_filters import rest_framework as filters
from furniture.models import Category, Furniture

class FurnitureFilter(filters.FilterSet):
    price_from = filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = filters.NumberFilter(lookup_expr='lte', field_name='price')
    categories = filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), field_name='category')    
    in_stock = filters.BooleanFilter(method='filter_in_stock', label='Только в наличии')

    class Meta:
        model = Furniture
        fields = ['_all_']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(receive_type=Furniture.IN_STOCK)
        return queryset
