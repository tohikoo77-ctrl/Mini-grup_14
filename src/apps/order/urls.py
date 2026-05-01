from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'order-products', views.OrderProductViewSet, basename='order-products')
router.register(r'addresses', views.AddressViewSet, basename='addresses')


urlpatterns = [
    path('', include(router.urls)),
]