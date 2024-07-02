from rest_framework.decorators import api_view
from api.filters import ProductFilter
from api.pagiantions import StadartPageNumberPagination
from api.parsers import NestedMultiPartParser
from api.serializers import ProductSerializer, ReadProductSerializer, CategorySerializer, TagSerializer, CreateProductSerializer
from market.models import Product,Category,Tag
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter



class ListCreateApiView(GenericAPIView):

    queryset = Product.objects.all()
    serializer_classes = {
       'get': ReadProductSerializer,
       'post': CreateProductSerializer,
    }
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [NestedMultiPartParser]
    pagination_class = StadartPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']
    search_fields = ['name', 'description', 'content']
    

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginated_queryset = self.paginate_queryset(queryset)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method.lower())


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def detail_update_delete_products(request, id):
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

