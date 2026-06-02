"""Admin configuration for catalog models."""

from django.contrib import admin

from .models import Category, Product, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing categories."""

    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing tags."""

    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for managing products and their relations."""

    list_display = ("name", "category", "price", "is_active", "created_at")
    list_filter = ("category", "tags", "is_active")
    search_fields = ("name", "description", "category__name", "tags__name")
    filter_horizontal = ("tags",)
    autocomplete_fields = ("category",)
    list_select_related = ("category",)
    readonly_fields = ("created_at",)
