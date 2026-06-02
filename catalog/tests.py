"""Tests for the catalog application."""

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Tag


class ProductListViewTests(TestCase):
    """Integration tests for the catalog product list page."""

    def setUp(self):
        """Create reusable catalog fixtures for search and filtering scenarios."""
        self.url = reverse("catalog:product_list")

        # Categories cover the primary filter branch used by the page.
        self.electrical = Category.objects.create(
            name="Electrical Supplies",
            slug="electrical-supplies",
        )
        self.safety = Category.objects.create(
            name="Safety Equipment",
            slug="safety-equipment",
        )

        # Tags support both single-tag and combined filter test cases.
        self.low_voltage = Tag.objects.create(name="Low Voltage", slug="low-voltage")
        self.warehouse = Tag.objects.create(name="Warehouse", slug="warehouse")
        self.ppe = Tag.objects.create(name="PPE", slug="ppe")

        # This product is the main electrical match for category and tag filtering.
        self.cable = Product.objects.create(
            name="Armored Cable Roll",
            description="Low-voltage cable for warehouse retrofit projects.",
            category=self.electrical,
            price="189.99",
            is_active=True,
        )
        self.cable.tags.set([self.low_voltage, self.warehouse])

        # This product is the main combined-filter match.
        self.gloves = Product.objects.create(
            name="Cut-Resistant Gloves",
            description="Protective gloves for receiving teams and warehouse handling.",
            category=self.safety,
            price="18.60",
            is_active=True,
        )
        self.gloves.tags.set([self.ppe, self.warehouse])

        # This product shares category and tag overlap but should be excluded from
        # combined searches that target the gloves description.
        self.vest = Product.objects.create(
            name="Reflective Safety Vest",
            description="High-visibility vest for contractor safety checks.",
            category=self.safety,
            price="24.50",
            is_active=True,
        )
        self.vest.tags.set([self.ppe])

        # This product confirms inactive records are filtered out even when they
        # would otherwise match the query parameters.
        self.inactive_product = Product.objects.create(
            name="Inactive Test Product",
            description="Low-voltage inventory item that should not be listed.",
            category=self.electrical,
            price="10.00",
            is_active=False,
        )
        self.inactive_product.tags.set([self.low_voltage])

    def test_product_list_page_loads_successfully(self):
        """The product list page returns a successful response."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_products_appear_on_the_page(self):
        """The default listing renders every active fixture product."""
        response = self.client.get(self.url)

        self.assertContains(response, self.cable.name)
        self.assertContains(response, self.gloves.name)
        self.assertContains(response, self.vest.name)

    def test_search_by_description(self):
        """The `q` parameter searches product descriptions with partial text."""
        response = self.client.get(self.url, {"q": "receiving teams"})

        self.assertContains(response, self.gloves.name)
        self.assertNotContains(response, self.cable.name)
        self.assertNotContains(response, self.vest.name)

    def test_filtering_by_category_slug(self):
        """The `category` parameter restricts results to one category slug."""
        response = self.client.get(self.url, {"category": self.electrical.slug})

        self.assertContains(response, self.cable.name)
        self.assertNotContains(response, self.gloves.name)
        self.assertNotContains(response, self.vest.name)

    def test_filtering_by_tag_slug(self):
        """A tag slug filters the queryset to products linked to that tag."""
        response = self.client.get(self.url, {"tags": [self.low_voltage.slug]})

        self.assertContains(response, self.cable.name)
        self.assertNotContains(response, self.gloves.name)
        self.assertNotContains(response, self.vest.name)

    def test_combining_search_category_and_tag_filters(self):
        """Search, category, and tag filters work together as one narrowed query."""
        response = self.client.get(
            self.url,
            {
                "q": "warehouse",
                "category": self.safety.slug,
                "tags": [self.ppe.slug],
            },
        )

        self.assertContains(response, self.gloves.name)
        self.assertNotContains(response, self.cable.name)
        self.assertNotContains(response, self.vest.name)

    def test_inactive_products_do_not_appear(self):
        """Inactive products never appear, even when their description matches."""
        response = self.client.get(self.url, {"q": "inventory item"})

        self.assertNotContains(response, self.inactive_product.name)
        self.assertContains(response, "No products match the current search and filter criteria.")

    def test_unknown_category_slug_returns_empty_results(self):
        """An unknown category slug should not error and should return no matches."""
        response = self.client.get(self.url, {"category": "missing-category"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertContains(response, "No products match the current search and filter criteria.")

    def test_unknown_tag_slug_returns_empty_results(self):
        """An unknown tag slug should not error and should return no matches."""
        response = self.client.get(self.url, {"tags": ["missing-tag"]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertContains(response, "No products match the current search and filter criteria.")

    def test_valid_and_invalid_tag_slugs_can_be_mixed(self):
        """Invalid tag slugs should not prevent valid tag filters from matching."""
        response = self.client.get(
            self.url,
            {"tags": [self.low_voltage.slug, "missing-tag", self.low_voltage.slug]},
        )

        self.assertContains(response, self.cable.name)
        self.assertNotContains(response, self.gloves.name)
        self.assertEqual(response.context["selected_tags"], [self.low_voltage.slug, "missing-tag"])

    def test_query_parameters_with_sql_like_input_do_not_break_the_view(self):
        """Hostile-looking input should be treated as plain text and return safely."""
        response = self.client.get(
            self.url,
            {
                "q": "' OR 1=1 --",
                "category": "'; DROP TABLE catalog_category; --",
                "tags": ["') OR ('1'='1"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertContains(response, "No products match the current search and filter criteria.")


class ProductListEmptyStateTests(TestCase):
    """Edge-case tests for empty product and filter datasets."""

    def setUp(self):
        """Prepare the product list URL without creating any catalog fixtures."""
        self.url = reverse("catalog:product_list")

    def test_page_handles_no_products_categories_or_tags(self):
        """The page should render cleanly when the catalog is completely empty."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertQuerySetEqual(response.context["products"], [])
        self.assertQuerySetEqual(response.context["categories"], [])
        self.assertQuerySetEqual(response.context["tags"], [])
        self.assertContains(response, "No tags available.")
        self.assertContains(response, "No products match the current search and filter criteria.")
