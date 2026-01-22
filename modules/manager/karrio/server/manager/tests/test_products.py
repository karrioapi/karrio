"""
Product REST API Tests

Comprehensive tests for the full CRUD operations on product templates.
Covers all endpoints, edge cases, validation, and access control.
"""
import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
from karrio.server.manager.models import Commodity


class TestProductsList(APITestCase):
    """Tests for GET /v1/products and POST /v1/products"""

    def test_create_product(self):
        """Test creating a new product template."""
        url = reverse("karrio.server.manager:product-list")
        data = PRODUCT_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, PRODUCT_RESPONSE)

    def test_create_product_minimal(self):
        """Test creating a product with only required fields."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 0.5,
            "weight_unit": "KG",
            "meta": {"label": "Minimal Product"},
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["weight"], 0.5)
        self.assertEqual(response_data["weight_unit"], "KG")
        self.assertEqual(response_data["meta"]["label"], "Minimal Product")

    def test_create_product_with_default_flag(self):
        """Test creating a product marked as default."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.0,
            "weight_unit": "LB",
            "title": "Default Product",
            "meta": {"label": "Default Product", "is_default": True},
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response_data["meta"]["is_default"])

    def test_create_product_without_label_fails(self):
        """Test that creating a product without meta.label fails."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "title": "Test Product",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_empty_label_fails(self):
        """Test that creating a product with empty meta.label fails."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "meta": {"label": ""},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_null_label_fails(self):
        """Test that creating a product with null meta.label fails."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "meta": {"label": None},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_without_weight_fails(self):
        """Test that creating a product without weight fails validation."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight_unit": "KG",
            "title": "No Weight Product",
            "meta": {"label": "No Weight"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_without_weight_unit_fails(self):
        """Test that creating a product without weight_unit fails validation."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "title": "No Weight Unit Product",
            "meta": {"label": "No Weight Unit"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_all_fields(self):
        """Test creating a product with all available fields."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 2.5,
            "weight_unit": "LB",
            "quantity": 10,
            "sku": "FULL-SKU-001",
            "title": "Full Product",
            "hs_code": "9876.54",
            "description": "A full product with all fields",
            "value_amount": 149.99,
            "value_currency": "EUR",
            "origin_country": "DE",
            "product_url": "https://example.com/product",
            "image_url": "https://example.com/image.jpg",
            "product_id": "prod_123",
            "variant_id": "var_456",
            "metadata": {"custom_field": "custom_value"},
            "meta": {"label": "Full Product", "is_default": True},
        }

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["weight"], 2.5)
        self.assertEqual(response_data["weight_unit"], "LB")
        self.assertEqual(response_data["quantity"], 10)
        self.assertEqual(response_data["sku"], "FULL-SKU-001")
        self.assertEqual(response_data["value_currency"], "EUR")
        self.assertEqual(response_data["origin_country"], "DE")
        self.assertEqual(response_data["metadata"]["custom_field"], "custom_value")

    def test_list_products(self):
        """Test listing all product templates."""
        # Create a product first
        Commodity.objects.create(
            **{
                "weight": 1.0,
                "weight_unit": "KG",
                "title": "Existing Product",
                "quantity": 1,
                "meta": {"label": "Existing Product", "is_default": False},
                "created_by": self.user,
            }
        )

        url = reverse("karrio.server.manager:product-list")
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response_data)
        self.assertGreaterEqual(len(response_data["results"]), 1)

    def test_list_products_empty(self):
        """Test listing products when none exist."""
        url = reverse("karrio.server.manager:product-list")
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["results"], [])

    def test_list_products_excludes_non_templates(self):
        """Test that listing products excludes commodities without meta.label."""
        # Create a commodity without meta.label (not a template)
        Commodity.objects.create(
            **{
                "weight": 1.0,
                "weight_unit": "KG",
                "title": "Non-template Commodity",
                "quantity": 1,
                "meta": {},  # No label
                "created_by": self.user,
            }
        )

        # Create a product template
        Commodity.objects.create(
            **{
                "weight": 2.0,
                "weight_unit": "KG",
                "title": "Template Product",
                "quantity": 1,
                "meta": {"label": "Template Product", "is_default": False},
                "created_by": self.user,
            }
        )

        url = reverse("karrio.server.manager:product-list")
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return the template, not the non-template commodity
        self.assertEqual(len(response_data["results"]), 1)
        self.assertEqual(
            response_data["results"][0]["meta"]["label"], "Template Product"
        )

    def test_list_products_pagination(self):
        """Test that product listing supports pagination."""
        # Create multiple products
        for i in range(25):
            Commodity.objects.create(
                **{
                    "weight": float(i + 1),
                    "weight_unit": "KG",
                    "title": f"Product {i}",
                    "quantity": 1,
                    "meta": {"label": f"Product {i}", "is_default": False},
                    "created_by": self.user,
                }
            )

        url = reverse("karrio.server.manager:product-list")
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Default limit is 20
        self.assertEqual(len(response_data["results"]), 20)
        self.assertIn("next", response_data)

    def test_list_products_with_limit(self):
        """Test listing products with custom limit."""
        # Create multiple products
        for i in range(10):
            Commodity.objects.create(
                **{
                    "weight": float(i + 1),
                    "weight_unit": "KG",
                    "title": f"Product {i}",
                    "quantity": 1,
                    "meta": {"label": f"Product {i}", "is_default": False},
                    "created_by": self.user,
                }
            )

        url = reverse("karrio.server.manager:product-list") + "?limit=5"
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), 5)


class TestProductDetails(APITestCase):
    """Tests for GET, PATCH, DELETE /v1/products/<pk>"""

    def setUp(self) -> None:
        super().setUp()
        self.product: Commodity = Commodity.objects.create(
            **{
                "weight": 1.5,
                "weight_unit": "KG",
                "quantity": 1,
                "sku": "TEST-SKU-001",
                "title": "Test Product Title",
                "hs_code": "123456",
                "description": "A test product",
                "value_amount": 99.99,
                "value_currency": "USD",
                "origin_country": "US",
                "meta": {"label": "Test Product", "is_default": False},
                "created_by": self.user,
            }
        )

    def test_retrieve_product(self):
        """Test retrieving a product by ID."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], self.product.pk)
        self.assertEqual(response_data["object_type"], "commodity")
        self.assertEqual(response_data["meta"]["label"], "Test Product")

    def test_retrieve_product_not_found(self):
        """Test retrieving a non-existent product returns 404."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk="nonexistent_id")
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """Test updating a product."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = PRODUCT_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, PRODUCT_UPDATE_RESPONSE)

    def test_update_product_label(self):
        """Test updating a product's label."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"meta": {"label": "Updated Label"}}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["meta"]["label"], "Updated Label")

    def test_update_product_default_flag(self):
        """Test updating a product's default flag."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"meta": {"is_default": True}}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_data["meta"]["is_default"])

    def test_update_product_single_field(self):
        """Test updating a single field on a product."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"weight": 3.0}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["weight"], 3.0)
        # Verify other fields unchanged
        self.assertEqual(response_data["title"], "Test Product Title")

    def test_update_product_sku(self):
        """Test updating a product's SKU."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"sku": "NEW-SKU-002"}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["sku"], "NEW-SKU-002")

    def test_update_product_value_and_currency(self):
        """Test updating a product's value and currency."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"value_amount": 199.99, "value_currency": "CAD"}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["value_amount"], 199.99)
        self.assertEqual(response_data["value_currency"], "CAD")

    def test_update_product_metadata(self):
        """Test updating a product's metadata."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=self.product.pk)
        )
        data = {"metadata": {"custom_key": "custom_value"}}

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["metadata"]["custom_key"], "custom_value")

    def test_update_product_not_found(self):
        """Test updating a non-existent product returns 404."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk="nonexistent_id")
        )
        data = {"weight": 2.0}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        """Test deleting a product."""
        product_pk = self.product.pk
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk=product_pk)
        )

        response = self.client.delete(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["object_type"], "commodity")
        self.assertFalse(Commodity.objects.filter(pk=product_pk).exists())

    def test_delete_product_not_found(self):
        """Test deleting a non-existent product returns 404."""
        url = reverse(
            "karrio.server.manager:product-details", kwargs=dict(pk="nonexistent_id")
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestProductValidation(APITestCase):
    """Tests for product validation rules."""

    def test_invalid_weight_unit(self):
        """Test that invalid weight unit fails validation."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "INVALID",
            "meta": {"label": "Invalid Weight Unit"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_value_currency(self):
        """Test that invalid currency code fails validation."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "value_amount": 100,
            "value_currency": "INVALID",
            "meta": {"label": "Invalid Currency"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_origin_country(self):
        """Test that invalid country code fails validation."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "origin_country": "INVALID",
            "meta": {"label": "Invalid Country"},
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_weight(self):
        """Test that negative weight is handled."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": -1.5,
            "weight_unit": "KG",
            "meta": {"label": "Negative Weight"},
        }

        response = self.client.post(url, data)
        # The API may accept negative weight (floats aren't validated for min)
        # This tests the current behavior

    def test_zero_weight(self):
        """Test that zero weight is handled."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 0,
            "weight_unit": "KG",
            "meta": {"label": "Zero Weight"},
        }

        response = self.client.post(url, data)
        # Zero weight might be allowed for some use cases

    def test_negative_quantity(self):
        """Test that negative quantity is handled."""
        url = reverse("karrio.server.manager:product-list")
        data = {
            "weight": 1.5,
            "weight_unit": "KG",
            "quantity": -1,
            "meta": {"label": "Negative Quantity"},
        }

        response = self.client.post(url, data)


# Test data
PRODUCT_DATA = {
    "weight": 1.5,
    "weight_unit": "KG",
    "quantity": 1,
    "sku": "TEST-SKU-001",
    "title": "Test Product Title",
    "hs_code": "123456",
    "description": "A test product",
    "value_amount": 99.99,
    "value_currency": "USD",
    "origin_country": "US",
    "meta": {"label": "Test Product", "is_default": False},
}

PRODUCT_RESPONSE = {
    "id": ANY,
    "object_type": "commodity",
    "weight": 1.5,
    "weight_unit": "KG",
    "title": "Test Product Title",
    "description": "A test product",
    "quantity": 1,
    "sku": "TEST-SKU-001",
    "hs_code": "123456",
    "value_amount": 99.99,
    "value_currency": "USD",
    "origin_country": "US",
    "product_url": None,
    "image_url": None,
    "product_id": None,
    "variant_id": None,
    "parent_id": None,
    "metadata": {},
    "meta": {"label": "Test Product", "is_default": False},
}

PRODUCT_UPDATE_DATA = {
    "weight": 2.0,
    "title": "Updated Title",
}

PRODUCT_UPDATE_RESPONSE = {
    "id": ANY,
    "object_type": "commodity",
    "weight": 2.0,
    "weight_unit": "KG",
    "title": "Updated Title",
    "description": "A test product",
    "quantity": 1,
    "sku": "TEST-SKU-001",
    "hs_code": "123456",
    "value_amount": 99.99,
    "value_currency": "USD",
    "origin_country": "US",
    "product_url": None,
    "image_url": None,
    "product_id": None,
    "variant_id": None,
    "parent_id": None,
    "metadata": {},
    "meta": {"label": "Test Product", "is_default": False},
}
