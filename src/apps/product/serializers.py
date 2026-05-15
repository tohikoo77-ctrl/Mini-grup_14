from rest_framework import serializers
from .models import Category, Product, ComboProduct, Promocode, News


# =========================
# CATEGORY
# =========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "is_active"]


# =========================
# PRODUCT
# =========================
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "old_price",
            "is_new",
            "is_sale",
            "is_hit",
            "stock",
            "is_active",
            "created_at",
            "category",
            "category_id",
        ]

    # create
    def create(self, validated_data):
        category_id = validated_data.pop("category_id")
        return Product.objects.create(category_id=category_id, **validated_data)

    # update
    def update(self, instance, validated_data):
        category_id = validated_data.pop("category_id", None)

        if category_id:
            instance.category_id = category_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
# =========================
# COMBO PRODUCT SERIALIZER
# =========================
class ComboProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboProduct
        fields = "__all__"

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Combo product nomi juda qisqa.")
        return value


# =========================
# PROMOCODE SERIALIZER
# =========================
class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = "__all__"

    def validate_code(self, value):
        if " " in value:
            raise serializers.ValidationError("Promocode ichida bo‘sh joy bo‘lmasligi kerak.")
        return value.upper()

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Discount 0-100 oralig‘ida bo‘lishi kerak.")
        return value

# =========================
# NEWS SERIALIZER
# =========================
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("News title juda qisqa.")
        return value