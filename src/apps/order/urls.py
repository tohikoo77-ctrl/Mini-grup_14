from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderProductViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-products', OrderProductViewSet, basename='order-product')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
]