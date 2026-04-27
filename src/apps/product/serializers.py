from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Narx manfiy yoki nol bo'lishi mumkin emas!")
        return value

    def validate_sku(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("SKU kodi kamida 4 ta belgidan iborat bo'lishi shart.")
        return value