from rest_framework import routers

from shop.rest.viewsets import ProductViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'^products', ProductViewSet)
router.register(r'^categories', CategoryViewSet)