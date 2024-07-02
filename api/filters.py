from django_filters import rest_framework as filters
from market.models import Product


class ProductFilter(filters.FilterSet):

    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    # price = filters.NumericRangeFilter()

    class Meta:
        model = Product
        fields = (
            'tags',
            'category',
            'user',
            'receive_type',
            'rating',
            'is_published',
        )