from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Order, OrderProduct, Address
from .serializer import (
    OrderSerializer,
    OrderProductSerializer,
    AddressSerializer,
)

@extend_schema(tags=["orders"])
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

@extend_schema(tags=["order-products"])
class OrderProductViewSet(ModelViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderProduct.objects.filter(order__client=self.request.user)

@extend_schema(tags=["address"])
class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(order__client=self.request.user)
