from rest_framework.decorators import api_view
from api.filters import ProductFilter
from api.mixins import PaginationBreakerMixin, SerializerByActionMixin, SerializerByMethodMixin, UltraGenericAPIView
from api.pagiantions import StadartPageNumberPagination
from api.parsers import NestedMultiPartParser
from api.permissions import IsAdminOrReadOnly, IsAuthenticatedOrOwnerOrReadOnly, IsOwnerOrReadOnly
from api.serializers import ProductSerializer, ListProductSerializer, DetailProductSerializer, CategorySerializer, TagSerializer, CreateProductSerializer
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
from rest_framework.generics import GenericAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
  

class ProductViewSet(SerializerByActionMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_classes = {
        'list': ListProductSerializer,
        'retreive': DetailProductSerializer,
        'update': ProductSerializer,
        'create': CreateProductSerializer,
    }
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrOwnerOrReadOnly]
    parser_classes = [NestedMultiPartParser]
    pagination_class = StadartPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']
    search_fields = ['name', 'description', 'content']


class ListCreateCategoryApiView(GenericAPIView, SerializerByMethodMixin, PaginationBreakerMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StadartPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['']
    ordering_fields = ['name']
    search_fields = ['name']
    
    
    def get(self, request, *args, **kwargs):
        categories = self.filter_queryset(self.get_queryset())
        
        paginated_qs = self.paginate_queryset(categories)
        if paginated_qs is not None:
            serializer = self.get_serializer(paginated_qs, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUpdateDeleteCategoryApiView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(instance=category)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_eception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(instance=category, data=request.data, partial=False)
        serializer.is_valid(raise_eception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateTagApiView(GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StadartPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name']
    search_fields = ['name']

    def get(self, request, *args, **kwargs):
        tags = self.filter_queryset(self.get_queryset())
        
        paginated_qs = self.paginate_queryset(tags)
        if paginated_qs is not None:
            serializer = self.get_serializer(paginated_qs, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DetailUpdateDeleteTagApiView(GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        tag = self.get_object()
        serializer = self.get_serializer(instance=tag)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        tag = self.get_object()
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=False)