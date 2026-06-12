from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsCategoryViewSet, NewsViewSet

router = DefaultRouter()
router.register(r"categories", NewsCategoryViewSet, basename="news-category")
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls)),
]
