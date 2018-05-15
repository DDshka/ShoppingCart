from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from shop.models import Category, Product


class AbstractProductView(TemplateView):
  def get_context_data(self, product_id: int):
    requested_product = get_object_or_404(Product, id=product_id)
    product_categories = requested_product.categories.all()

    context = {
      "product": requested_product,
      "categories": product_categories
    }
    return context


class AbstractCategoryProductsView(TemplateView):
  def get_context_data(self, category_id: int):
    requested_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categories__in=[category_id])

    context = {
      'category': requested_category,
      'products': products,
    }
    return context

