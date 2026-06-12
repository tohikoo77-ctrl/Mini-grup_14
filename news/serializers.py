from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer

from .models import News, NewsCategory


class NewsCategorySerializer(serializers.ModelSerializer):
    news_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = NewsCategory
        fields = ["id", "name", "news_count"]

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Rubrika nomi kamida 2 ta harf bo'lishi kerak.")
        return value


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=NewsCategory.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source="product",
        queryset=Product.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "description",
            "content",
            "image",
            "category",
            "category_id",
            "product",
            "product_id",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Sarlavha kamida 3 ta harf bo'lishi kerak.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Qisqacha matn kamida 10 ta harf bo'lishi kerak.")
        return value
