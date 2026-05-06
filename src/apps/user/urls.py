from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
    path('auth/verify/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('auth/resend-code/', ResendVerificationAPIView.as_view(), name='resend-verification'),
    path("login/", login_view),
    path("logout/", logout_view),
    path("forget-password/", forget_password),
    path("reset-password/", reset_password),
]