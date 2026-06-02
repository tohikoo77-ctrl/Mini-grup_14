from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Order, OrderProduct, Address
from .serializer import (
    OrderSerializer,
    OrderProductSerializer,
    AddressSerializer,
)

@extend_schema_view(
    list=extend_schema(summary="List my orders"),
    create=extend_schema(summary="Create order"),
    retrieve=extend_schema(summary="Get order details"),
    update=extend_schema(summary="Update order"),
    partial_update=extend_schema(summary="Partially update order"),
    destroy=extend_schema(summary="Delete order"),
)
@extend_schema(tags=["orders"])
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(client__user=self.request.user)

    def perform_create(self, serializer):
        client = getattr(self.request.user, "client", None)
        if client is None:
            raise PermissionDenied("Buyurtma yaratish uchun client profili kerak.")
        serializer.save(client=client)

@extend_schema(tags=["order-products"])
class OrderProductViewSet(ModelViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrderProduct.objects.none()
        return OrderProduct.objects.filter(order__client__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data.get("order")
        if order is None:
            raise ValidationError({"order": "Order ID is required."})
        if order.client.user != self.request.user:
            raise PermissionDenied("You can add products only to your own orders.")
        serializer.save()

    def perform_update(self, serializer):
        order = serializer.validated_data.get("order", serializer.instance.order)
        if order.client.user != self.request.user:
            raise PermissionDenied("You can update products only on your own orders.")
        serializer.save()

@extend_schema(tags=["address"])
class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Address.objects.none()
        return Address.objects.filter(order__client__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data.get("order")
        if order is None:
            raise ValidationError({"order": "Order ID is required."})
        if order.client.user != self.request.user:
            raise PermissionDenied("You can add addresses only to your own orders.")
        serializer.save()

    def perform_update(self, serializer):
        order = serializer.validated_data.get("order", serializer.instance.order)
        if order.client.user != self.request.user:
            raise PermissionDenied("You can update addresses only on your own orders.")
        serializer.save()
