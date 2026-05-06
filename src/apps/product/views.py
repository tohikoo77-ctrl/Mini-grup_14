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

from .serializers import CategorySerializer, ProductSerializer


# =========================
# CATEGORY VIEWSET
# =========================
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


# =========================
# PRODUCT VIEWSET + FILTER
# =========================
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # filters
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if category:
            queryset = queryset.filter(category_id=category)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

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
