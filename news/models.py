from django.db import models

from product.models import Product


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "News category"
        verbose_name_plural = "News categories"

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        related_name="news_items",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="news_items",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
