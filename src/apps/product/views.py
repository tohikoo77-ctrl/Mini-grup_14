from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ComboProductViewSet(ModelViewSet):
    queryset = ComboProduct.objects.all()
    serializer_class = ComboProductSerializer


class PromocodeViewSet(ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer