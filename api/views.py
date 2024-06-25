from rest_framework.decorators import api_view
from api.filters import ProductFilter
from api.parsers import NestedMultiPartParser
from api.serializers import ProductSerializer, ReadProductSerializer, CategorySerializer, TagSerializer, CreateProductSerializer
from market.models import Product,Category,Tag
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes, authentication_classes


@api_view(['GET', 'POST'])
@parser_classes([NestedMultiPartParser])
def list_products(request):
    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data, context={'request': request})
        # if serializer.is_valid():
        #     product = serializer.save()
        #     return Response(serializer.data, status.HTTP_201_CREATED)

        # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

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
 
    serializer = ReadProductSerializer(products, many=True, context={'request': request})
    data = {
        'count': qs_count,
        'page_count': pagin.num_pages,
        'results': serializer.data
    }

    return Response(data)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def detail_products(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method in ['PATCH', 'PUT']:
        serializer = ProductSerializer(
            instance=product, 
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    serializer = ProductSerializer(product, context={'request': request})
    # pprint(*serializer.data)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def create_category(request):
    if request.method == 'POST':
        data = request.data
        serializer = CategorySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def detail_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method in ['PATCH', 'PUT']:
        serializer = CategorySerializer(
            instance=category, 
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    serializer = CategorySerializer(category, context={'request': request})
    return Response(serializer.data)



@api_view(['GET', 'POST'])
def create_tag(request):
    if request.method == 'POST':
        data = request.data
        serializer = TagSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def detail_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method in ['PATCH', 'PUT']:
        serializer = TagSerializer(
            instance=tag, 
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            tag = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
   
    serializer = TagSerializer(tag, context={'request': request})
    return Response(serializer.data)

