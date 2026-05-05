from rest_framework import serializers
from .models import Brand, Category, Product


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
# PRODUCT SERIALIZER
# =========================
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    brand_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

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
