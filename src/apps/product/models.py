from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Kategoriya nomi")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name

    name = models.CharField(max_length=30)
    description = models.TextField()

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    is_hit = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_sale = models.BooleanField(default=False)

    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
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
