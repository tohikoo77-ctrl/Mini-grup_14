from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    ComboProductViewSet,
    PromocodeViewSet,
    NewsViewSet,
)
router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"combos", ComboProductViewSet, basename="combo")
router.register(r"promocodes", PromocodeViewSet, basename="promocode")
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls)),
]