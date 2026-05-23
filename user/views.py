from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

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
    ForgetPasswordSerializer,
    LeadStatusSerializer,
    LoginSerializer,
    PasswordUpdateSerializer,
    RegisterSerializer,
    ResendVerificationSerializer,
    ResetPasswordSerializer,
    SellerSerializer,
    SellerWalletSerializer,
    TagSerializer,
    UserProfileUpdateSerializer,
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
        getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        [user.email],
        fail_silently=True,
    )


def find_user_for_password_reset(validated_data):
    if validated_data.get("email"):
        return get_object_or_404(User, email=validated_data["email"])
    return get_object_or_404(User, username=validated_data["username"])


class RegisterAPIView(APIView):
    @extend_schema(
        request=RegisterSerializer,
        responses={201: {"description": "User registered successfully"}},
        description="Register a new user account",
    )
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
                "verification_code": verification.code,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyCodeAPIView(APIView):
    @extend_schema(
        request=VerifyCodeSerializer,
        responses={200: {"description": "Email verified successfully"}},
        description="Verify user email with verification code",
    )
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
    @extend_schema(
        request=ResendVerificationSerializer,
        responses={200: {"description": "Verification code sent successfully"}},
        description="Resend email verification code",
    )
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
                "verification_code": verification.code,
            },
            status=status.HTTP_200_OK,
        )


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserProfileUpdateSerializer},
        description="Get current authenticated user profile",
    )
    def get(self, request):
        serializer = UserProfileUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UserProfileUpdateSerializer,
        responses={200: UserProfileUpdateSerializer},
        description="Update current authenticated user profile information",
    )
    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "User profile updated successfully.",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PasswordUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PasswordUpdateSerializer,
        responses={200: {"description": "Password updated successfully"}},
        description="Update current authenticated user's password",
    )
    def post(self, request):
        serializer = PasswordUpdateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )


class ForgetPasswordAPIView(APIView):
    @extend_schema(
        request=ForgetPasswordSerializer,
        responses={200: {"description": "Password reset code sent"}},
        description="Create and send password reset code",
    )
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = find_user_for_password_reset(serializer.validated_data)

        verification = EmailVerificationCode.objects.create(user=user)
        send_verification_email(user, verification.code)

        return Response(
            {
                "detail": "Password reset code sent.",
                "username": user.username,
                "email": user.email,
                "reset_code": verification.code,
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(APIView):
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: {"description": "Password reset successfully"}},
        description="Reset user password by reset code",
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = find_user_for_password_reset(serializer.validated_data)

        verification = EmailVerificationCode.objects.filter(
            user=user,
            code=serializer.validated_data["code"],
            is_used=False,
            expires_at__gte=timezone.now(),
        ).first()

        if not verification:
            return Response(
                {"detail": "Invalid or expired code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        verification.is_used = True
        verification.save(update_fields=["is_used"])

        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK,
        )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

@extend_schema(tags=["auth-login"])
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
    
@extend_schema(tags=["users"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema(tags=["seller"])
class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

@extend_schema(tags=["seller-wallet"])
class SellerWalletViewSet(ModelViewSet):
    queryset = SellerWallet.objects.all()
    serializer_class = SellerWalletSerializer

@extend_schema(tags=["client"])
class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

@extend_schema(tags=["cart"])
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@extend_schema(tags=["favorite"])
class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

@extend_schema(tags=["tag"])
class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@extend_schema(tags=["lead-status"])
class LeadStatusViewSet(ModelViewSet):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer

@extend_schema(tags=["seller-dashboard"])
class SellerView(APIView):
    permission_classes = [IsSeller]

    @extend_schema(
        responses={200: {"description": "Seller dashboard access granted"}},
        description="Access seller-only content",
    )
    def get(self, request):
        return Response({"message": "Only sellers can see this"})
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    data = json.loads(request.body)

    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login success"})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)
    
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@csrf_exempt
def forget_password(request):
    data = json.loads(request.body or "{}")
    serializer = ForgetPasswordSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    user = find_user_for_password_reset(serializer.validated_data)
    code = EmailVerificationCode.objects.create(user=user)
    send_verification_email(user, code.code)
    return JsonResponse(
        {
            "message": "Password reset code sent",
            "username": user.username,
            "email": user.email,
            "reset_code": code.code,
        }
    )

@csrf_exempt
def reset_password(request):
    data = json.loads(request.body or "{}")
    serializer = ResetPasswordSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    user = find_user_for_password_reset(serializer.validated_data)
    otp = EmailVerificationCode.objects.filter(
        user=user,
        code=serializer.validated_data["code"],
        is_used=False,
        expires_at__gte=timezone.now(),
    ).first()
    if not otp:
        return JsonResponse({"error": "Invalid or expired code"}, status=400)

    user.set_password(serializer.validated_data["new_password"])
    user.save(update_fields=["password"])

    otp.is_used = True
    otp.save(update_fields=["is_used"])

    return JsonResponse({"message": "Password reset successful"})
