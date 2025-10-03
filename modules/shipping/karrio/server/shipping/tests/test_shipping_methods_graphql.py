from unittest.mock import ANY
import karrio.server.graph.tests.base as base
import karrio.server.shipping.models as models


class TestShippingMethodsGraphQL(base.GraphTestCase):
    """Test GraphQL CRUD operations for shipping methods."""

    def setUp(self):
        super().setUp()
        # Create test shipping method via GraphQL
        response = self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method {
                  id
                  slug
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Express Shipping",
                    "description": "Fast delivery service",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_priority",
                    "carrier_ids": ["canadapost"],
                    "carrier_options": {"insurance": 100},
                    "metadata": {"created_for": "testing"},
                    "is_active": True,
                }
            },
        )
        self.shipping_method = models.ShippingMethod.objects.get(
            id=response.data["data"]["create_shipping_method"]["shipping_method"]["id"]
        )

    def test_query_shipping_methods_list(self):
        """Test querying list of shipping methods."""
        response = self.query(
            """
            query GetShippingMethods($filter: ShippingMethodFilter) {
              shipping_methods(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    slug
                    description
                    carrier_code
                    carrier_service
                    carrier_ids
                    carrier_options
                    metadata
                    is_active
                    test_mode
                  }
                }
              }
            }
            """,
            variables={"filter": {"first": 10}},
        )

        expected_response = {
            "data": {
                "shipping_methods": {
                    "edges": [
                        {
                            "node": {
                                "id": self.shipping_method.id,
                                "name": "Express Shipping",
                                "slug": "express-shipping",
                                "description": "Fast delivery service",
                                "carrier_code": "canadapost",
                                "carrier_service": "canadapost_priority",
                                "carrier_ids": ["canadapost"],
                                "carrier_options": {"insurance": 100},
                                "metadata": {"created_for": "testing"},
                                "is_active": True,
                                "test_mode": False,
                            }
                        }
                    ]
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_query_single_shipping_method(self):
        """Test querying a single shipping method by ID."""
        response = self.query(
            """
            query GetShippingMethod($id: String!) {
              shipping_method(id: $id) {
                id
                name
                slug
                description
                carrier_code
                carrier_service
                carrier_ids
                carrier_options
                metadata
                is_active
                test_mode
              }
            }
            """,
            variables={"id": self.shipping_method.id},
        )

        expected_response = {
            "data": {
                "shipping_method": {
                    "id": self.shipping_method.id,
                    "name": "Express Shipping",
                    "slug": "express-shipping",
                    "description": "Fast delivery service",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_priority",
                    "carrier_ids": ["canadapost"],
                    "carrier_options": {"insurance": 100},
                    "metadata": {"created_for": "testing"},
                    "is_active": True,
                    "test_mode": False,
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_basic_shipping_method(self):
        """Test creating a basic shipping method."""
        response = self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method {
                  id
                  name
                  slug
                  description
                  carrier_code
                  carrier_service
                  carrier_ids
                  carrier_options
                  metadata
                  is_active
                  test_mode
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Standard Shipping",
                    "description": "Regular delivery service",
                    "carrier_code": "ups",
                    "carrier_service": "ups_ground",
                    "carrier_ids": ["ups_package"],
                    "carrier_options": {"signature_required": True},
                    "metadata": {"priority": "low"},
                    "is_active": True,
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_method": {
                    "shipping_method": {
                        "id": ANY,
                        "name": "Standard Shipping",
                        "slug": ANY,
                        "description": "Regular delivery service",
                        "carrier_code": "ups",
                        "carrier_service": "ups_ground",
                        "carrier_ids": ["ups_package"],
                        "carrier_options": {"signature_required": True},
                        "metadata": {"priority": "low"},
                        "is_active": True,
                        "test_mode": False,
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_shipping_method_with_minimal_fields(self):
        """Test creating a shipping method with only required fields."""
        response = self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method {
                  id
                  name
                  carrier_code
                  carrier_service
                  is_active
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Economy Shipping",
                    "carrier_code": "fedex",
                    "carrier_service": "fedex_ground",
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_method": {
                    "shipping_method": {
                        "id": ANY,
                        "name": "Economy Shipping",
                        "carrier_code": "fedex",
                        "carrier_service": "fedex_ground",
                        "is_active": ANY,
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_create_shipping_method_with_multiple_carriers(self):
        """Test creating a shipping method with multiple carrier IDs."""
        response = self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method {
                  id
                  name
                  carrier_code
                  carrier_service
                  carrier_ids
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Multi-Carrier Shipping",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_regular_parcel",
                    "carrier_ids": ["canadapost", "ups_package", "fedex_express"],
                }
            },
        )

        expected_response = {
            "data": {
                "create_shipping_method": {
                    "shipping_method": {
                        "id": ANY,
                        "name": "Multi-Carrier Shipping",
                        "carrier_code": "canadapost",
                        "carrier_service": "canadapost_regular_parcel",
                        "carrier_ids": ["canadapost", "ups_package", "fedex_express"],
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_update_shipping_method(self):
        """Test updating an existing shipping method."""
        response = self.query(
            """
            mutation UpdateShippingMethod($data: UpdateShippingMethodMutationInput!) {
              update_shipping_method(input: $data) {
                shipping_method {
                  id
                  name
                  description
                  is_active
                  carrier_options
                }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipping_method.id,
                    "name": "Updated Express Shipping",
                    "description": "Updated description",
                    "is_active": False,
                    "carrier_options": {"insurance": 200, "signature_required": True},
                }
            },
        )

        expected_response = {
            "data": {
                "update_shipping_method": {
                    "shipping_method": {
                        "id": self.shipping_method.id,
                        "name": "Updated Express Shipping",
                        "description": "Updated description",
                        "is_active": False,
                        "carrier_options": {"insurance": 200, "signature_required": True},
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_update_shipping_method_metadata(self):
        """Test updating shipping method metadata."""
        response = self.query(
            """
            mutation UpdateShippingMethod($data: UpdateShippingMethodMutationInput!) {
              update_shipping_method(input: $data) {
                shipping_method {
                  id
                  metadata
                }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipping_method.id,
                    "metadata": {"created_for": "testing", "updated": True, "version": 2},
                }
            },
        )

        expected_response = {
            "data": {
                "update_shipping_method": {
                    "shipping_method": {
                        "id": self.shipping_method.id,
                        "metadata": {"created_for": "testing", "updated": True, "version": 2},
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_update_shipping_method_carrier_service(self):
        """Test updating carrier service and related fields."""
        response = self.query(
            """
            mutation UpdateShippingMethod($data: UpdateShippingMethodMutationInput!) {
              update_shipping_method(input: $data) {
                shipping_method {
                  id
                  carrier_code
                  carrier_service
                  carrier_ids
                }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipping_method.id,
                    "carrier_code": "ups",
                    "carrier_service": "ups_express",
                    "carrier_ids": ["ups_package"],
                }
            },
        )

        expected_response = {
            "data": {
                "update_shipping_method": {
                    "shipping_method": {
                        "id": self.shipping_method.id,
                        "carrier_code": "ups",
                        "carrier_service": "ups_express",
                        "carrier_ids": ["ups_package"],
                    }
                }
            }
        }

        self.assertDictEqual(response.data, expected_response)

    def test_delete_shipping_method(self):
        """Test deleting a shipping method."""
        response = self.query(
            """
            mutation DeleteShippingMethod($data: DeleteMutationInput!) {
              delete_shipping_method(input: $data) {
                id
              }
            }
            """,
            variables={"data": {"id": self.shipping_method.id}},
        )

        expected_response = {
            "data": {"delete_shipping_method": {"id": self.shipping_method.id}}
        }

        self.assertDictEqual(response.data, expected_response)

        # Verify method is deleted
        self.assertFalse(
            models.ShippingMethod.objects.filter(id=self.shipping_method.id).exists()
        )

    def test_query_shipping_methods_with_filter(self):
        """Test querying shipping methods with search filter."""
        # Create additional shipping methods via GraphQL
        self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method { id }
              }
            }
            """,
            variables={
                "data": {
                    "name": "UPS Ground Shipping",
                    "carrier_code": "ups",
                    "carrier_service": "ups_ground",
                    "is_active": True,
                }
            },
        )

        response = self.query(
            """
            query GetShippingMethods($filter: ShippingMethodFilter) {
              shipping_methods(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    carrier_code
                  }
                }
              }
            }
            """,
            variables={"filter": {"search": "Express", "first": 10}},
        )

        # Should only return the Express shipping method
        self.assertEqual(len(response.data["data"]["shipping_methods"]["edges"]), 1)
        self.assertEqual(
            response.data["data"]["shipping_methods"]["edges"][0]["node"]["name"],
            "Express Shipping",
        )
