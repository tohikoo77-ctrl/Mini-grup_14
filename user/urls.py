from django.urls import include, path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CartViewSet,
    ClientViewSet,
    FavoriteViewSet,
    ForgetPasswordAPIView,
    LeadStatusViewSet,
    PasswordUpdateAPIView,
    RegisterAPIView,
    ResendVerificationAPIView,
    ResetPasswordAPIView,
    SellerViewSet,
    SellerWalletViewSet,
    TagViewSet,
    UserProfileAPIView,
    UserViewSet,
    VerifyCodeAPIView,
    forget_password,
    login_view,
    logout_view,
    reset_password,
)

TokenObtainPairView = extend_schema_view(
    post=extend_schema(tags=["auth-login"], summary="Obtain JWT access/refresh tokens"),
)(TokenObtainPairView)

TokenRefreshView = extend_schema_view(
    post=extend_schema(tags=["auth-login"], summary="Refresh JWT access token"),
)(TokenRefreshView)

router = DefaultRouter()

router.register("users", UserViewSet, basename="user")
router.register("sellers", SellerViewSet, basename="seller")
router.register("wallets", SellerWalletViewSet, basename="wallet")
router.register("clients", ClientViewSet, basename="client")
router.register("carts", CartViewSet, basename="cart")
router.register("favorites", FavoriteViewSet, basename="favorite")
router.register("tags", TagViewSet, basename="tag")
router.register("lead-status", LeadStatusViewSet, basename="lead-status")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("auth/update-password/", PasswordUpdateAPIView.as_view(), name="update-password"),
    path("auth/verify/", VerifyCodeAPIView.as_view(), name="verify-code"),
    path("auth/resend-code/", ResendVerificationAPIView.as_view(), name="resend-verification"),
    path("auth/forget-password/", ForgetPasswordAPIView.as_view(), name="forget-password-api"),
    path("auth/reset-password/", ResetPasswordAPIView.as_view(), name="reset-password-api"),
    path("login/", login_view),
    path("logout/", logout_view),
    path("forget-password/", forget_password),
    path("reset-password/", reset_password),
]
