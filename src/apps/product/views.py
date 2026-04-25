from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, ComboProduct, Promocode, News
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ComboProductSerializer,
    PromocodeSerializer,
    NewsSerializer
)


# =========================
# CATEGORY VIEWSET
# =========================
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


# =========================
# PRODUCT VIEWSET (ADVANCED)
# =========================
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "is_new", "is_sale", "is_hit", "category"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # custom filtering (optional advanced logic)
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        try:
            if min_price:
                queryset = queryset.filter(price__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass # Ignore invalid numeric inputs

        return queryset


# =========================
# COMBO PRODUCT VIEWSET
# =========================
class ComboProductViewSet(ModelViewSet):
    queryset = ComboProduct.objects.select_related("combo", "item").all()
    serializer_class = ComboProductSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["price"]


# =========================
# PROMOCODE VIEWSET
# =========================
class PromocodeViewSet(ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer

    filter_backends = [SearchFilter]
    search_fields = ["code"]


# =========================
# NEWS VIEWSET
# =========================
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at"]