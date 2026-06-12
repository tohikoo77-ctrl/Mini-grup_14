from django.contrib import admin

from .models import News, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "product", "is_published", "created_at", "updated_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "description", "content")
