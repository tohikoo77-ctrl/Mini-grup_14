from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, OrderProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-products", OrderProductViewSet, basename="order-product")
router.register(r"addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
]
