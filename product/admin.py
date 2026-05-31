from django.contrib import admin
from .models import Brand, Category, Discount, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "price", "image", "category", "brand", "created_at")
    list_filter = ("category", "brand")
    search_fields = ("name", "sku", "description", "category__name", "brand__name")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "product",
        "discount_type",
        "value",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = ("discount_type", "is_active", "starts_at", "ends_at")
    search_fields = ("name", "product__name")
