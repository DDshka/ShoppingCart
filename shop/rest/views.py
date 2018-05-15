from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductDetailsView(APIView):
  def get(self, request, product_id):
    from shop.models import Product
    from .serializers import ProductSerializer

    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)

    return Response(serializer.data)


class CategoryDetailsView(APIView):
  def get(self, request, category_id):
    from shop.models import Category
    from .serializers import CategorySerializer

    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category)

    return Response(serializer.data)