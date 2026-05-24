from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from .models import Brand, Category, Discount, Product
from .serializers import BrandSerializer, CategorySerializer, DiscountSerializer, ProductSerializer
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view


# =========================
# CATEGORY VIEWSET
# =========================
@extend_schema(tags=["product-category"])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


@extend_schema(tags=["brands"])
class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]


# =========================
# PRODUCT VIEWSET (ADVANCED)
# =========================
@extend_schema_view(
    list=extend_schema(
        summary="List products",
        description="Mahsulotlarni qidirish, filterlash va narx bo'yicha saralash.",
        parameters=[
            OpenApiParameter("min_price", OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
            OpenApiParameter("max_price", OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
        ],
    ),
    create=extend_schema(summary="Create product"),
    retrieve=extend_schema(summary="Get product details"),
    update=extend_schema(summary="Update product"),
    partial_update=extend_schema(summary="Partially update product"),
    destroy=extend_schema(summary="Delete product"),
)
@extend_schema(tags=["products"])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category", "brand").all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "brand"]
    search_fields = ["name", "sku", "description", "category__name", "brand__name"]
    ordering_fields = ["id", "name", "price", "created_at", "updated_at"]

    def get_queryset(self):
        now = timezone.now()
        queryset = super().get_queryset().annotate(
            active_discounts_count=Count(
                "discounts",
                filter=Q(discounts__is_active=True)
                & (Q(discounts__starts_at__isnull=True) | Q(discounts__starts_at__lte=now))
                & (Q(discounts__ends_at__isnull=True) | Q(discounts__ends_at__gte=now)),
            )
        )

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


@extend_schema_view(
    list=extend_schema(
        summary="List discounts",
        description=(
            "Discountlarni ko'rish. `product`, `discount_type`, `is_active`, "
            "`search`, `ordering` filterlari mavjud."
        ),
    ),
    create=extend_schema(summary="Create discount"),
    retrieve=extend_schema(summary="Get discount details"),
    update=extend_schema(summary="Update discount"),
    partial_update=extend_schema(summary="Partially update discount"),
    destroy=extend_schema(summary="Delete discount"),
)
@extend_schema(tags=["discounts"])
class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.select_related("product").all()
    serializer_class = DiscountSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["product", "discount_type", "is_active"]
    search_fields = ["name", "product__name"]
    ordering_fields = ["id", "name", "value", "starts_at", "ends_at", "created_at"]
