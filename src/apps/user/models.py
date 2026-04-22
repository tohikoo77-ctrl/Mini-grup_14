from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.product.models import Product


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)

    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=13)

    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    date_of_birth = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller")

    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)

    longitude = models.CharField(max_length=30)
    latitude = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


class SellerWallet(models.Model):
    seller = models.OneToOneField(
        Seller, on_delete=models.CASCADE, related_name="wallet"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_take = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")

    orders_count = models.IntegerField(default=0)
    returns_products_count = models.IntegerField(default=0)

    phone_number = models.CharField(max_length=13)

    from_where = models.CharField(max_length=150, blank=True, null=True)


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="carts")
    "product = models.ForeignKey(Product, on_delete=models.CASCADE)"

    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)


class Favorite(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="favorites"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class LeadStatus(models.Model):
    name = models.CharField(max_length=50)
