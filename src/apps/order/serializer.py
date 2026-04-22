from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, OrderProduct, Address


# ---------------------------
# ORDER PRODUCT
# ---------------------------
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'price']

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity 0 dan katta bo‘lishi kerak")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price 0 dan katta bo‘lishi kerak")
        return value


# ---------------------------
# ADDRESS
# ---------------------------
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'in_tashkent',
            'address_name',
            'longitude',
            'latitude',
            'street',
            'home',
            'apartment',
        ]


# ---------------------------
# ORDER (FULL LOGIC)
# ---------------------------
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'address',
            'total_price',
            'status',
            'payment_type',
            'is_active',
            'created_at',
            'products',
        ]
        read_only_fields = ['id', 'created_at']

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        address_data = validated_data.pop('address', None)

        order = Order.objects.create(**validated_data)

        # products
        total_price = 0
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
            total_price += float(product_data.get('price', 0)) * product_data.get('quantity', 1)

        # address
        if address_data:
            Address.objects.create(order=order, **address_data)

        # update total price
        order.total_price = total_price
        order.save()

        return order

    # ---------------- UPDATE ----------------
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        address_data = validated_data.pop('address', None)

        # update order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update products
        if products_data is not None:
            instance.products.all().delete()

            total_price = 0
            for product_data in products_data:
                OrderProduct.objects.create(order=instance, **product_data)
                total_price += float(product_data.get('price', 0)) * product_data.get('quantity', 1)

            instance.total_price = total_price
            instance.save()

        # update address
        if address_data is not None:
            Address.objects.update_or_create(
                order=instance,
                defaults=address_data
            )

        return instance