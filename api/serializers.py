from rest_framework import serializers

from market.models import Product, Category, Tag
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProductSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    # category1 = CategorySerializer(source='category')
    # category = serializers.CharField(source='category.name')
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = '__all__'