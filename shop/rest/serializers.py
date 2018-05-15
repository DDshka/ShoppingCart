from rest_framework import serializers

# Serializers define the API representation.
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField, HyperlinkedRelatedField


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    from shop.models import Category
    model = Category
    fields = ('id', 'name')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
  categories = CategorySerializer(many=True)

  class Meta:
      from shop.models import Product
      model = Product
      fields = ('id', 'name', 'price', 'categories')


class CartProductSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
      from shop.models import Product
      model = Product
      fields = ('id', 'name', 'price', 'categories')
