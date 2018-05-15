from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
  from shop.rest.serializers import ProductSerializer
  from shop.models import Product

  queryset = Product.objects.all()
  serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
  from shop.rest.serializers import CategorySerializer
  from shop.models import Category

  queryset = Category.objects.all()
  serializer_class = CategorySerializer