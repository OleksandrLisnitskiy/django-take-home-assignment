"""Database models for the catalog application."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    """A product grouping used to organize the catalog."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """A descriptive label that can be attached to many products."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """A sellable catalog item with category and optional tags."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["category", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=Decimal("0.00")),
                name="product_price_gte_0",
            ),
        ]

    def __str__(self) -> str:
        return self.name
