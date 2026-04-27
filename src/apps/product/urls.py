# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import *

# router = DefaultRouter()
# router.register('categories', CategoryViewSet)
# router.register('products', ProductViewSet)
# router.register('combos', ComboProductViewSet)
# router.register('promocodes', PromocodeViewSet)
# router.register('news', NewsViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]