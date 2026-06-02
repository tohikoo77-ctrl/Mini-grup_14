from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from product.models import Category, Product
from user.models import Client as UserClient
from user.models import User
from .models import Address, Order, OrderProduct


class OrderApiTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.user = User.objects.create_user(
            username="order_user",
            email="order@example.com",
            password="StrongPass123",
            first_name="Order",
            last_name="User",
            phone_number="+998901111111",
            is_active=True,
            is_verified=True,
        )
        self.client_profile = UserClient.objects.create(
            user=self.user,
            phone_number="+998901111111",
        )
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone Pro",
            sku="PHONE-TEST",
            price="1200000.00",
            category=category,
        )
        self.api.force_authenticate(self.user)

    def test_create_order_with_nested_products_and_address(self):
        response = self.api.post(
            reverse("order-list"),
            {
                "payment_type": "cash",
                "is_active": True,
                "products": [
                    {
                        "product": self.product.id,
                        "quantity": 2,
                        "price": "1000000.00",
                    }
                ],
                "address": {
                    "in_tashkent": True,
                    "address_name": "Home",
                    "longitude": "69.240100",
                    "latitude": "41.299500",
                    "street": "Amir Temur",
                    "home": "1",
                    "apartment": "10",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.client, self.client_profile)
        self.assertEqual(order.products.count(), 1)
        self.assertEqual(order.addresses.count(), 1)
        self.assertEqual(str(order.total_price), "2000000.00")

    def test_create_order_product_requires_owned_order(self):
        order = Order.objects.create(
            client=self.client_profile,
            payment_type="cash",
        )

        response = self.api.post(
            reverse("order-product-list"),
            {
                "order": order.id,
                "product": self.product.id,
                "quantity": 1,
                "price": "1000000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(OrderProduct.objects.filter(order=order).exists())

    def test_create_address_requires_owned_order(self):
        order = Order.objects.create(
            client=self.client_profile,
            payment_type="cash",
        )

        response = self.api.post(
            reverse("address-list"),
            {
                "order": order.id,
                "in_tashkent": True,
                "address_name": "Office",
                "longitude": "69.240100",
                "latitude": "41.299500",
                "street": "Mustaqillik",
                "home": "2",
                "apartment": "20",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Address.objects.filter(order=order).exists())
