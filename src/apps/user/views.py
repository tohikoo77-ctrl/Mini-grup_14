from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import (
    Cart,
    Client,
    EmailVerificationCode,
    Favorite,
    LeadStatus,
    Seller,
    SellerWallet,
    Tag,
    User,
)
from .permissions import IsSeller
from .serializers import (
    CartSerializer,
    ClientSerializer,
    FavoriteSerializer,
    LeadStatusSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResendVerificationSerializer,
    SellerSerializer,
    SellerWalletSerializer,
    TagSerializer,
    UserSerializer,
    VerifyCodeSerializer,
)


def send_verification_email(user, code):
    subject = "Your verification code"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        f"Your verification code is: {code}\n"
        "This code will expire in 24 hours.\n\n"
        "If you did not register, please ignore this message."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        verification = EmailVerificationCode.objects.create(user=user)
        send_verification_email(user, verification.code)

        return Response(
            {
                "detail": "Registered successfully. Check your email for the verification code.",
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyCodeAPIView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        user = get_object_or_404(User, email=email)

        verification = EmailVerificationCode.objects.filter(
            user=user,
            code=code,
            is_used=False,
            expires_at__gte=timezone.now(),
        ).first()

        if not verification:
            return Response(
                {"detail": "Invalid or expired verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification.is_used = True
        verification.save()

        user.is_verified = True
        user.is_active = True
        user.save()

        return Response(
            {"detail": "Email verified successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )


class ResendVerificationAPIView(APIView):
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)

        if user.is_verified:
            return Response(
                {"detail": "This account is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification = EmailVerificationCode.objects.create(user=user)
        send_verification_email(user, verification.code)

        return Response(
            {
                "detail": "A new verification code was sent to your email.",
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


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