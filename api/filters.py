import django_filters
from market.models import Product


class ProductFilter(django_filters.FilterSet):

    from_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # price = django_filters.NumericRangeFilter()

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