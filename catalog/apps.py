"""App configuration for the catalog application."""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Default Django app configuration for catalog."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
