from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import EmailVerificationCode, User


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_FAIL_SILENTLY=False,
)
class AuthEmailVerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.verify_url = reverse("verify-code")
        self.token_url = reverse("token-obtain-pair")

    def register_payload(self):
        return {
            "username": "postman_user",
            "email": "Postman.User@example.com",
            "password": "StrongPass123",
            "first_name": "Postman",
            "last_name": "Tester",
            "phone_number": "+998901234567",
            "role": "user",
            "date_of_birth": "2000-01-01",
        }

    def test_register_sends_verification_email_and_keeps_user_inactive(self):
        response = self.client.post(
            self.register_url,
            self.register_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "postman.user@example.com")
        self.assertEqual(len(mail.outbox), 1)

        user = User.objects.get(username="postman_user")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertEqual(user.email, "postman.user@example.com")
        self.assertTrue(EmailVerificationCode.objects.filter(user=user).exists())

    def test_unverified_user_cannot_get_jwt_token(self):
        self.client.post(self.register_url, self.register_payload(), format="json")

        response = self.client.post(
            self.token_url,
            {"username": "postman_user", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Email is not verified", str(response.data))

    def test_verify_email_then_get_jwt_token(self):
        self.client.post(self.register_url, self.register_payload(), format="json")
        user = User.objects.get(username="postman_user")
        code = EmailVerificationCode.objects.filter(user=user).latest("created_at")

        verify_response = self.client.post(
            self.verify_url,
            {"email": user.email, "code": code.code},
            format="json",
        )
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_verified)

        token_response = self.client.post(
            self.token_url,
            {"username": "postman_user", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)
