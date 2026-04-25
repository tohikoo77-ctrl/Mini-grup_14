from decimal import Decimal

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

    def validate(self, attrs):
        quantity = attrs.get('quantity', 0)
        price = attrs.get('price', 0)

        if quantity <= 0:
            raise ValidationError({"quantity": "Quantity 0 dan katta bo‘lishi kerak"})

        if price <= 0:
            raise ValidationError({"price": "Price 0 dan katta bo‘lishi kerak"})

        return attrs


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
# ORDER
# ---------------------------
class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'total_price',
            'status',
            'payment_type',
            'is_active',
            'created_at',
            'products',
            'address',
        ]
        read_only_fields = ['id', 'client', 'created_at', 'total_price']

    # ---------------- PRIVATE METHOD ----------------
    def _calculate_total_price(self, products_data):
        total = Decimal("0")
        for item in products_data:
            price = Decimal(item.get('price', 0))
            quantity = item.get('quantity', 1)
            total += price * quantity
        return total

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        address_data = validated_data.pop('address', None)

        order = Order.objects.create(**validated_data)

        # products
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)

        # address
        if address_data:
            Address.objects.create(order=order, **address_data)

        # total price
        order.total_price = self._calculate_total_price(products_data)
        order.save()

        return order

    # ---------------- UPDATE ----------------
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', None)
        address_data = validated_data.pop('address', None)

        # update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # update products
        if products_data is not None:
            instance.products.all().delete()

            for product_data in products_data:
                OrderProduct.objects.create(order=instance, **product_data)

            instance.total_price = self._calculate_total_price(products_data)

        # update address
        if address_data:
            Address.objects.update_or_create(
                order=instance,
                defaults=address_data
            )

        instance.save()
        return instance