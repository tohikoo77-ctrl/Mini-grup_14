from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .views import RegisterView, LoginView
from .views import login_view, logout_view, forget_password, reset_password

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('sellers', SellerViewSet)
router.register('wallets', SellerWalletViewSet)
router.register('clients', ClientViewSet)
router.register('carts', CartViewSet)
router.register('favorites', FavoriteViewSet)
router.register('tags', TagViewSet)
router.register('lead-status', LeadStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', UserProfileAPIView.as_view(), name='user-profile'),
    path('auth/update-password/', PasswordUpdateAPIView.as_view(), name='update-password'),
    path('auth/verify/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('auth/resend-code/', ResendVerificationAPIView.as_view(), name='resend-verification'),
    path('auth/forget-password/', ForgetPasswordAPIView.as_view(), name='forget-password-api'),
    path('auth/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password-api'),
    path("login/", login_view),
    path("logout/", logout_view),
    path("forget-password/", forget_password),
    path("reset-password/", reset_password),
]
