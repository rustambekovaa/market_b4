from pprint import pprint
from rest_framework.decorators import api_view

from api.filters import ProductFilter
from api.serializers import ProductSerializer
from market.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()

    search = request.GET.get('search', None)

    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(content__icontains=search)
        )

    ordering_list = ['price', 'name']

    ordering = request.GET.get('ordering', None)

    if ordering and ordering.split('-')[1] in ordering_list:
        products = products.order_by(ordering)

    filter_set = ProductFilter(data=request.GET, queryset=products)
    products = filter_set.qs   

    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 24))

    qs_count = products.count()

    pagin = Paginator(products, page_size)
    products = pagin.get_page(page)
 
    serializer = ProductSerializer(products, many=True, context={'request': request})
    data = {
        'count': qs_count,
        'page_count': pagin.num_pages,
        'results': serializer.data
    }

    return Response(data)


@api_view(['GET'])
def detail_products(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product, context={'request': request})
    # pprint(*serializer.data)
    return Response(serializer.data)