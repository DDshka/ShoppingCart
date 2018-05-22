from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q

from shop.abstracts.views import AbstractProductView, AbstractCategoryProductsView
from shop.forms import *
from shop.models import *


PAGINATION_STEP = 10

class HomeView(TemplateView):
  """Main (home) page"""
  template_name = "home.html"

  def get_context_data(self, **kwargs):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
      'categories': categories,
      'products': products
    }
    return context


class ProductView(AbstractProductView):
  """Product details view"""
  template_name = "product.html"

  def get_context_data(self, product_id: int):
    context = super().get_context_data(product_id)
    context['form'] = AddToCartForm(initial={"product": product_id})
    return context


class CategoryProductsView(AbstractCategoryProductsView):
  """Category details view
  Renders product list of a current category"""
  template_name = "category_products.html"


class CartDelete(View):
  def get(self):
    return HttpResponse("Get not supported")

  def post(self, request, index: int):
    try:
      del request.session['products'][int(index)]
      request.session.modified = True
    except:
      print("something wrong in CartDelete post method.")
    finally:
      return redirect("/cart")


class CartView(TemplateView):
  template_name = "cart.html"

  def post(self, request):
    form = AddToCartForm(request.POST)
    if form.is_valid():
      if 'products' not in request.session:
        request.session['products'] = []

      product = form.cleaned_data.get('product')
      request.session['products'].append(product.to_json())
      request.session.modified = True

      return redirect("/cart")

    return HttpResponse("Something went wrong")

  def get_context_data(self):
    products = Product.get_from_session(self.request)

    total = 0
    for product in products:
      total += product.price

    context = {
      'products': products,
      'total': total,
    }
    return context


class SearchView(TemplateView):
  """Handles user search"""
  template_name = "search.html"

  def get(self, request, *args, **kwargs):
    if request.GET:
      return self.do_search(request)
    else:
      context = {
        'form': SearchForm()
      }
      return render(request, "search.html", context)

  def do_search(self, request):
    form = SearchForm(request.GET)
    if form.is_valid():
      order = form.cleaned_data.get('order')  # default 'name'
      page = form.cleaned_data.get('page')
      conditions = self._build_condition(form)

      from django.contrib.postgres.search import SearchVector
      products = Product.objects\
        .annotate(search=SearchVector('name', 'description'))\
        .filter(conditions)\
        .distinct()\
        .order_by('name')
      paginator = Paginator(products, PAGINATION_STEP)
      products = paginator.page(page)

      context = {
        "form": self._reset_form(form),
        "products": products,
      }
      return render(request, "search.html", context)
    else:
      raise ValidationError("Something went wrong")

  def _build_condition(self, form: SearchForm) -> Q:
    query = form.cleaned_data.get('q')
    requested_categories = form.cleaned_data.get('categories')

    conditions = Q()
    if query:
      conditions.add(
        Q(search=query), Q.AND
      )

    if Category.ALL_CATEGORIES not in requested_categories:
      conditions.add(
        Q(categories__in=requested_categories), Q.AND
      )

    return conditions

  def _reset_form(self, form:SearchForm) -> SearchForm:
    return SearchForm(initial={
      'q': form.cleaned_data.get('q'),
      'categories': form.cleaned_data.get('categories')
    })
