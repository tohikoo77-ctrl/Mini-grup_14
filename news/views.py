from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import News, NewsCategory
from .serializers import NewsCategorySerializer, NewsSerializer


@extend_schema(tags=["news-category"])
class NewsCategoryViewSet(ModelViewSet):
    queryset = NewsCategory.objects.annotate(news_count=Count("news_items")).all()
    serializer_class = NewsCategorySerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "news_count"]


@extend_schema_view(
    list=extend_schema(summary="List news"),
    create=extend_schema(summary="Create news"),
    retrieve=extend_schema(summary="Get news details"),
    update=extend_schema(summary="Update news"),
    partial_update=extend_schema(summary="Partially update news"),
    destroy=extend_schema(summary="Delete news"),
)
@extend_schema(tags=["news"])
class NewsViewSet(ModelViewSet):
    queryset = News.objects.select_related("category").all()
    serializer_class = NewsSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "product", "is_published"]
    search_fields = ["title", "description", "content", "category__name", "product__name"]
    ordering_fields = ["id", "title", "created_at", "updated_at"]
