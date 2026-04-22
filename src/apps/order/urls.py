from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'orders', views.OrderModelView, basename='orders')
router.register(r'order-products', views.OrderProductModelView, basename='order-products')
router.register(r'addresses', views.AddressModelView, basename='addresses')


urlpatterns = [
    path('', include(router.urls)),
]