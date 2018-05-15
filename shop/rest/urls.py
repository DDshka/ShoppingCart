from django.conf.urls import url

from shop.rest.methods import sign_s3
from .views import *

urlpatterns = [
  url(r'^products/(?P<product_id>\d+)$', ProductDetailsView.as_view()),
  url(r'^categories/(?P<category_id>\d+)$', CategoryDetailsView.as_view()),
  url(r'^sign_s3', sign_s3),
]