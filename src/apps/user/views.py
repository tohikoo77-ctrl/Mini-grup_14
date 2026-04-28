from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .permissions import IsSeller
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data["username"],
            password=request.data["password"]
        )

        if user:
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerWalletViewSet(ModelViewSet):
    queryset = SellerWallet.objects.all()
    serializer_class = SellerWalletSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class LeadStatusViewSet(ModelViewSet):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer


class SellerView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        return Response({"message": "Only sellers can see this"})