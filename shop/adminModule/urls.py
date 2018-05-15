from django.conf.urls import url

from shop.adminModule.views import *


urlpatterns = [
  url(r'^$', AdminView.as_view(),
      name="admin-home"),

  url(r'^categories$', CategoriesView.as_view(),
      name="admin-categories"),

  url(r'^categories/(?P<category_id>\d+)$', CategoryProductsView.as_view(),
      name="admin-category-details"),

  url(r'^products$', ProductsView.as_view(),
      name='admin-products'),

  url(r'^products/(?P<product_id>\d+)$', ProductView.as_view(),
      name="admin-product-details"),

  url(r'^images$', ImagesView.as_view(),
      name="admin-images"),

  url(r'^addCategory$', AddCategoryView.as_view(),
      name='admin-add-category'),

  url(r'^addProduct$', AddProductView.as_view(),
      name='admin-add-product'),

  url(r'^addImage$', AddImageView.as_view(),
      name='admin-add-image'),

  url(r'^deleteProduct/(?P<pk>\d+)$', DeleteProductView.as_view(),
      name="delete-product"),

  url(r'^deleteCategory/(?P<pk>\d+)$', DeleteCategoryView.as_view(),
      name="delete-category"),

  url(r'^deleteImage/(?P<pk>\d+)$', DeleteImage.as_view(),
      name="delete-image"),

  url(r'^removeProductCategory/(?P<product_id>\d+)/(?P<category_id>\d+)$', RemoveProductCategory.as_view(),
      name="remove-product-category"),

  url(r'^addProductToCategory/(?P<category_id>\d+)$', AddProductToCategory.as_view(),
      name="add-product-to-category-list"),

  url(r'^addProductToCategory/(?P<category_id>\d+)/(?P<product_id>\d+)$', AddProductToCategory.as_view(),
      name="add-product-to-category"),

  url(r'^addCategoryToProduct/(?P<product_id>\d+)$', AddCategoryToProduct.as_view(),
      name="add-category-to-product-list"),

  url(r'^addCategoryToProduct/(?P<product_id>\d+)/(?P<category_id>\d+)$', AddCategoryToProduct.as_view(),
      name="add-category-to-product"),

  url(r'^search', SearchView.as_view(),
      name="admin-search"),

  url(r'^updateCategory/(?P<pk>\d+)', UpdateCategory.as_view(),
      name="update-category"),
]