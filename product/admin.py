from django.contrib import admin
# Supplier so'zini bu yerdan o'chirib tashlang:
from .models import Product, Category, Brand 

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(Supplier)  <-- Buni o'chirib tashlang yoki oldiga # qo'ying