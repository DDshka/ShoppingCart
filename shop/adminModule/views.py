from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView

from shop.abstracts.views import AbstractProductView, AbstractCategoryProductsView
from shop.forms import *
from shop.models import *


class AdminView(TemplateView):
  """Main admin page"""
  template_name = "admin/admin.html"

  def get_context_data(self):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
      "products": products,
      "categories": categories,
    }
    return context


class CategoriesView(ListView):
  """Admin list of categories"""

  template_name = "admin/admin_categories.html"
  context_object_name = 'categories'

  def get_queryset(self):
    categories = Category.objects.all()
    return categories


class ProductsView(ListView):
  """Admin list of products view"""

  template_name = "admin/admin_products.html"
  context_object_name = 'products'

  def get_queryset(self):
    return Product.objects.all()


class SearchView(ListView):
  """Admin search view"""
  template_name = "admin/admin_products.html"
  context_object_name = 'products'

  def get_queryset(self):
    query = self.request.GET.get('q')
    if query:
      return Product.objects.filter(name__icontains=query)
    else:
      return Product.objects.all()


class ProductView(AbstractProductView):
  """Admin product details view"""
  template_name = "admin/admin_product.html"


class CategoryProductsView(AbstractCategoryProductsView):
  """Admin product list for current category"""
  template_name = "admin/admin_category_products.html"


class ImagesView(ListView):
  template_name = "admin/admin_images.html"
  queryset = Image.objects.all()
  context_object_name = "images"


class AddCategoryView(CreateView):
  """Admin view to create category"""
  form_class = CategoryForm
  template_name = "admin/admin_add_category.html"
  success_url = reverse_lazy('admin-home')


class AddProductView(CreateView):
  """Admin view to create product"""
  form_class = ProductForm
  template_name = "admin/admin_add_product.html"
  success_url = reverse_lazy('admin-home')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['images_form'] = ProductImagesForm()
    return context



class DeleteProductView(DeleteView):
  """Deletes product from database
  Redirects to /adminWebPage/products
  """
  model = Product
  success_url = reverse_lazy("admin-products")


class DeleteCategoryView(DeleteView):
  """Deletes category from database.
  All products with current category will not be deleted
  Redirects to /adminWebPage/categories"""
  model = Category
  success_url = reverse_lazy("admin-categories")


class RemoveProductCategory(View):
  """Allows to remove product from category
  Redirects user to previous visited page
  """
  def post(self, request, product_id: int, category_id: int):
    """
    Args:
      product_id (int): id of current product
      category_id (int): id of category to remove
    """
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(id=category_id)
    product.categories.remove(category)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # back to previous page


class AddProductToCategory(View):
  """Allows to add products to category
  on category details page"""
  def get(self, request, category_id: int):
    """Renders list of available products to add to current category
    (These products must have any category excluding current)

    Args:
        category_id (int): Id of a category where products will be added
    """
    category = Category.objects.get(id=category_id)
    products = Product.objects.exclude(categories__in=[category_id])
    context = {
      "category": category,
      "products": products,
    }
    return render(request, "admin/admin_available_products_to_add.html", context)

  def post(self, request, category_id: int, product_id: int):
    """Adds product to category.

    Args:
      category_id (int): Id of a category where product will be added
      product_id (int): Id of a product to add
    """
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(id=category_id)
    product.categories.add(category)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddCategoryToProduct(View):
  """Allows to add categories
  on product details page"""
  def get(self, request, product_id: int):
    """Renders list of available categories to add for current product

    Args:
      product_id (int): Id of a current product
    """
    product = Product.objects.get(id=product_id)
    currentCategories = [x.id for x in product.categories.all()]
    availableCategories = Category.objects.exclude(id__in=currentCategories)
    context = {
      'categories': availableCategories,
      'product': product
    }
    return render(request, "admin/admin_available_categories_to_add.html", context)

  def post(self, request, product_id: int, category_id: int):
    """Adds category to product.

    Args:
      product_id (int): Id of a product
      category_id (int): Id of a category to add
    """
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(id=category_id)
    product.categories.add(category)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddImageView(CreateView):
  model = Image
  fields = ['file']
  template_name = "admin/admin_add_image.html"
  success_url = reverse_lazy("admin-home")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    images = Image.objects.all()
    context['images'] = images

    return context


class DeleteImage(DeleteView):
  model = Image
  success_url = reverse_lazy("admin-images")


class UpdateCategory(UpdateView):
  model = Category
  fields = ('name', 'description')
  template_name = 'admin/admin_add_category.html'


class AddUser(CreateView):
  model = User
  fields = ('info',)
  template_name = 'admin/admin_add_image.html'