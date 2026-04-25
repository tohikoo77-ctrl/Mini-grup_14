from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)  # FIX
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # FIX

    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_hit = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_sale = models.BooleanField(default=False)

    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ComboProduct(models.Model):
    combo = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="combo_items"
    )
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="contained_in_combos"
    )

    is_active = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.combo.name


class Promocode(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="promocode"
    )
    discount_int = models.CharField(max_length=3,unique=True,blank=True)
    discount_per = models.CharField(max_length=2 , unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return F"{self.discount_int}  | {self.discount_per}"

class News(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="news"
    )
