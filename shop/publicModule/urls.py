from django.conf.urls import url

from shop.publicModule.views import *


urlpatterns = [
  url(r'^$', HomeView.as_view(),
      name="home"),

  url(r'^categories/(?P<category_id>\d+)$', CategoryProductsView.as_view(),
      name="category-details"),

  url(r'^cart$', CartView.as_view(),
      name="cart"),

  url(r'^cart/add$', CartView.as_view(),
      name="add-to-cart"),

  url(r'^cart/delete/(?P<index>\d+)$', CartDelete.as_view(),
      name="delete-from-cart"),

  url(r'^products/(?P<product_id>\d+)$', ProductView.as_view(),
      name="product-details"),

  url(r'^search', SearchView.as_view(),
      name="search"),
]