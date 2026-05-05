from rest_framework import serializers
from .models import Category, Product, ComboProduct, Promocode, News


# =========================
# CATEGORY SERIALIZER
# =========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "is_active"]

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Kategoriya nomi kamida 2 ta harf bo‘lishi kerak.")
        return value

    def validate(self, attrs):
        parent = attrs.get("parent")
        name = attrs.get("name")

        if parent and parent.name == name:
            raise serializers.ValidationError("Kategoriya o‘zining parenti bo‘la olmaydi.")

        return attrs


# =========================
# PRODUCT SERIALIZER
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
            "is_hit",
            "is_new",
            "is_sale",
            "stock",
            "is_active",
            "image",
            "created_at",
            "category",
            "category_id",
        ]

    # name validation
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product nomi kamida 3 ta harf bo‘lishi kerak.")
        return value

    # price validation
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx 0 dan katta bo‘lishi kerak.")
        return value

    # stock validation
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock manfiy bo‘lishi mumkin emas.")
        return value

    # global validation
    def validate(self, attrs):
        price = attrs.get("price")
        old_price = attrs.get("old_price")

        if old_price and old_price < price:
            raise serializers.ValidationError("Old price yangi narxdan kichik bo‘lishi mumkin emas.")

        if attrs.get("is_sale") and not old_price:
            raise serializers.ValidationError("Sale bo‘lsa old_price bo‘lishi shart.")

        return attrs

    # create logic
    def create(self, validated_data):
        category_id = validated_data.pop("category_id")
        return Product.objects.create(category_id=category_id, **validated_data)


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