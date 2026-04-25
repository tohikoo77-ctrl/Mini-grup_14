from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderProduct, Address
from .serializer import (
    OrderSerializer,
    OrderProductSerializer,
    AddressSerializer,
)


class OrderModelView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)


class OrderProductModelView(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderProduct.objects.filter(order__client=self.request.user)


class AddressModelView(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(order__client=self.request.user)