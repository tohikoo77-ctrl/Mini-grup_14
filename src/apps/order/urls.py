from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderModelView, OrderProductModelView, AddressModelView

router = DefaultRouter()
router.register(r'orders', OrderModelView, basename='order')
router.register(r'order-products', OrderProductModelView, basename='order-product')
router.register(r'addresses', AddressModelView, basename='address')

urlpatterns = [
    path('', include(router.urls)),
]