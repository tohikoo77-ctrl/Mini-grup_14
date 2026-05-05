from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderProduct, Address
from .serializer import (
    OrderSerializer,
    OrderProductSerializer,
    AddressSerializer,
)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderProductViewSet(ModelViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderProduct.objects.filter(order__client=self.request.user)


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(order__client=self.request.user)
