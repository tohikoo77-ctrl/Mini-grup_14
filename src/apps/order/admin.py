from django.contrib import admin
from .models import Order, Address, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    max_num = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline, AddressInline]
    list_display = (
        'id',
        'client',
        'total_price',
        'status',
        'payment_type',
        'is_active'
    )

    search_fields = (
        'client__username',
        'addresses__address_name',
        'status',
    )

    list_filter = (
        'status',
        'payment_type',
        'is_active',
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'address_name',
        'street',
        'home',
        'apartment',
    )

    search_fields = (
        'address_name',
        'street',
        'home',
        'apartment',
        'order__id',
    )

    list_filter = (
        'in_tashkent',
        'street',
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )

    search_fields = (
        'order__id',
        'product__name',
    )

    list_filter = (
        'order',
    )