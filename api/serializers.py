from rest_framework import serializers

from market.models import Product, Category, ProductAttribute, ProductImage, Tag
from django.contrib.auth.models import User
from pprint import pprint


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


class ReadProductSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    # category1 = CategorySerializer(source='category')
    # category = serializers.CharField(source='category.name')
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    
class AttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ImagesForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ('product',)


class CreateProductSerializer(serializers.ModelSerializer):

    attributes = AttributeForProductSerializer(many=True)
    images = ImagesForProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):


        attributes = validated_data.pop('attributes')
        images = validated_data.pop('images')

        product = super().create(validated_data)

        for attribute in attributes:
            ProductAttribute.objects.create(**attribute, product=product)

        for image in images:
            image = image['image']
            product_image = ProductImage.objects.create(product=product)
            product_image.image.save(image.name, image)
            product_image.save()

        return product