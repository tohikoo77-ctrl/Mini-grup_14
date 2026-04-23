from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ComboProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboProduct
        fields = '__all__'

class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'