from rest_framework import serializers
from decimal import Decimal

from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field

from .models import Brand, Category, Discount, Product


# =========================
# CATEGORY SERIALIZER
# =========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Kategoriya nomi kamida 2 ta harf bo‘lishi kerak.")
        return value


# =========================
# BRAND SERIALIZER
# =========================
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Brand nomi kamida 2 ta harf bo'lishi kerak.")
        return value


# =========================
# PRODUCT SERIALIZER
# =========================
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    brand_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    active_discounts_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "price",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "active_discounts_count",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product nomi kamida 3 ta harf bo‘lishi kerak.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx 0 dan katta bo‘lishi kerak.")
        return value

    def create(self, validated_data):
        category_id = validated_data.pop("category_id")
        brand_id = validated_data.pop("brand_id", None)
        return Product.objects.create(category_id=category_id, brand_id=brand_id, **validated_data)


# =========================
# DISCOUNT SERIALIZER
# =========================
class DiscountSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "product",
            "product_name",
            "discount_type",
            "value",
            "starts_at",
            "ends_at",
            "is_active",
            "final_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "product_name", "final_price", "created_at", "updated_at"]

    @extend_schema_field(serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True))
    def get_final_price(self, obj):
        if not obj.product:
            return None

        price = obj.product.price
        if obj.discount_type == Discount.DiscountType.PERCENTAGE:
            final_price = price - (price * obj.value / Decimal("100"))
        else:
            final_price = price - obj.value

        return max(final_price, Decimal("0.00"))

    def validate(self, attrs):
        discount_type = attrs.get("discount_type", getattr(self.instance, "discount_type", None))
        value = attrs.get("value", getattr(self.instance, "value", None))
        starts_at = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends_at = attrs.get("ends_at", getattr(self.instance, "ends_at", None))

        if value is not None and value <= 0:
            raise ValidationError({"value": "Discount qiymati 0 dan katta bo'lishi kerak."})
        if (
            discount_type == Discount.DiscountType.PERCENTAGE
            and value is not None
            and value > 100
        ):
            raise ValidationError({"value": "Foizli discount 100 dan oshmasligi kerak."})
        if starts_at and ends_at and ends_at <= starts_at:
            raise ValidationError({"ends_at": "Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak."})

        return attrs
