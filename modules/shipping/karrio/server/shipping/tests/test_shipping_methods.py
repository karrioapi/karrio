import json
from unittest.mock import ANY, patch
from django.urls import reverse
from rest_framework import status

import karrio.server.manager.models as manager_models
import karrio.server.shipping.models as models
import karrio.server.graph.tests.base as base
import karrio.core.models as sdk


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
                    "carrier_id": "canadapost",
                    "carrier_options": {"insurance": 100},
                    "metadata": {"created_for": "testing"},
                    "is_active": True,
                }
            },
        )

        # Check for errors
        if response.data.get("errors"):
            raise Exception(f"GraphQL errors: {response.data['errors']}")

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
                    carrier_id
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
                                "slug": ANY,
                                "description": "Fast delivery service",
                                "carrier_code": "canadapost",
                                "carrier_service": "canadapost_priority",
                                "carrier_id": "canadapost",
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
                carrier_id
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
                    "slug": ANY,
                    "description": "Fast delivery service",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_priority",
                    "carrier_id": "canadapost",
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
                  carrier_id
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
                    "carrier_id": "ups_package",
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
                        "carrier_id": "ups_package",
                        "carrier_options": {"signature_required": True},
                        "metadata": {"priority": "low"},
                        "is_active": True,
                        "test_mode": False,
                    }
                }
            }
        }

        self.assertResponseNoErrors(response)
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

        self.assertResponseNoErrors(response)
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
                  carrier_id
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Multi-Carrier Shipping",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_regular_parcel",
                    "carrier_id": "canadapost",
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
                        "carrier_id": "canadapost",
                    }
                }
            }
        }

        self.assertResponseNoErrors(response)
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
                        "carrier_options": {
                            "insurance": 200,
                            "signature_required": True,
                        },
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
                    "metadata": {
                        "created_for": "testing",
                        "updated": True,
                        "version": 2,
                    },
                }
            },
        )

        expected_response = {
            "data": {
                "update_shipping_method": {
                    "shipping_method": {
                        "id": self.shipping_method.id,
                        "metadata": {
                            "created_for": "testing",
                            "updated": True,
                            "version": 2,
                        },
                    }
                }
            }
        }

        self.assertResponseNoErrors(response)
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
                  carrier_id
                }
              }
            }
            """,
            variables={
                "data": {
                    "id": self.shipping_method.id,
                    "carrier_code": "ups",
                    "carrier_service": "ups_express",
                    "carrier_id": "ups_package",
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
                        "carrier_id": "ups_package",
                    }
                }
            }
        }

        self.assertResponseNoErrors(response)
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

        self.assertResponseNoErrors(response)
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
        self.assertResponseNoErrors(response)
        self.assertEqual(len(response.data["data"]["shipping_methods"]["edges"]), 1)
        self.assertEqual(
            response.data["data"]["shipping_methods"]["edges"][0]["node"]["name"],
            "Express Shipping",
        )


class TestShippingMethodList(base.GraphTestCase):
    def test_list_shipping_methods(self):
        # Create shipping methods via GraphQL API
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
                    "name": "Express Shipping",
                    "description": "Fast delivery",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_priority",
                    "carrier_id": "canadapost",
                    "is_active": True,
                }
            },
        )
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
                    "name": "Standard Shipping",
                    "description": "Regular delivery",
                    "carrier_code": "ups",
                    "carrier_service": "ups_ground",
                    "carrier_id": "ups_package",
                    "is_active": True,
                }
            },
        )

        url = reverse("karrio.server.shipping:shipping-method-list")
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], 2)
        self.assertDictEqual(response_data["results"][0], SHIPPING_METHOD_RESPONSE_1)
        self.assertDictEqual(response_data["results"][1], SHIPPING_METHOD_RESPONSE_2)


class TestBuyShippingMethodLabel(base.GraphTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Create shipping method via GraphQL API
        response = self.query(
            """
            mutation CreateShippingMethod($data: CreateShippingMethodMutationInput!) {
              create_shipping_method(input: $data) {
                shipping_method {
                  id
                  name
                  slug
                }
              }
            }
            """,
            variables={
                "data": {
                    "name": "Standard Shipping",
                    "description": "Standard shipping method",
                    "carrier_code": "canadapost",
                    "carrier_service": "canadapost_priority",
                    "carrier_id": "canadapost",
                    "carrier_options": {"insurance": 100},
                    "metadata": {"key": "value"},
                    "is_active": True,
                }
            },
        )

        # Check for errors
        if response.data.get("errors"):
            raise Exception(f"GraphQL errors: {response.data['errors']}")

        self.shipping_method = models.ShippingMethod.objects.get(
            id=response.data["data"]["create_shipping_method"]["shipping_method"]["id"]
        )

    def test_buy_method_label(self):
        url = reverse(
            "karrio.server.shipping:buy-method-label",
            kwargs=dict(pk=self.shipping_method.pk),
        )
        data = LABEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [RETURNED_RATES_VALUE, CREATED_SHIPMENT_RESPONSE]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertResponseNoErrors(response) # type: ignore
        self.assertDictEqual(response_data, BUY_METHOD_LABEL_RESPONSE)


SHIPPING_METHOD_RESPONSE_1 = {
    "id": ANY,
    "object_type": "shipping-method",
    "name": "Standard Shipping",
    "description": "Regular delivery",
    "carrier_code": "ups",
    "carrier_service": "ups_ground",
    "carrier_id": "ups_package",
    "carrier_options": {},
    "metadata": {},
    "is_active": True,
    "test_mode": ANY,
    "created_at": ANY,
}

SHIPPING_METHOD_RESPONSE_2 = {
    "id": ANY,
    "object_type": "shipping-method",
    "name": "Express Shipping",
    "description": "Fast delivery",
    "carrier_code": "canadapost",
    "carrier_service": "canadapost_priority",
    "carrier_id": "canadapost",
    "carrier_options": {},
    "metadata": {},
    "is_active": True,
    "test_mode": ANY,
    "created_at": ANY,
}

LABEL_DATA = {
    "recipient": {
        "address_line1": "125 Church St",
        "person_name": "John Poop",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
    },
    "shipper": {
        "address_line1": "5840 Oak St",
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "phone_number": "514 000 9999",
        "city": "Vancouver",
        "country_code": "CA",
        "postal_code": "V6M2V9",
        "residential": False,
        "state_code": "BC",
    },
    "parcels": [
        {
            "weight": 1,
            "weight_unit": "KG",
            "package_preset": "canadapost_corrugated_small_box",
        }
    ],
    "payment": {"currency": "CAD", "paid_by": "sender"},
}

RETURNED_RATES_VALUE = [
    [
        sdk.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            total_charge=106.71,
            extra_charges=[
                sdk.ChargeDetails(amount=13.92, currency="CAD", name="Duty and taxes"),
                sdk.ChargeDetails(amount=2.7, currency="CAD", name="Fuel surcharge"),
                sdk.ChargeDetails(amount=-11.74, currency="CAD", name="SMB Savings"),
                sdk.ChargeDetails(amount=-9.04, currency="CAD", name="Discount"),
                sdk.ChargeDetails(amount=101.83, currency="CAD", name="Base surcharge"),
            ],
        )
    ],
    [],
]

CREATED_SHIPMENT_RESPONSE = (
    sdk.ShipmentDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        tracking_number="123456789012",
        shipment_identifier="123456789012",
        docs=dict(label="==apodifjoefr"),
    ),
    [],
)

BUY_METHOD_LABEL_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": "/v1/trackers/canadapost/123456789012",
    "shipper": {
        "id": ANY,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-9999",
        "state_code": "BC",
        "residential": False,
        "street_number": None,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "recipient": {
        "id": ANY,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "residential": False,
        "street_number": None,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "return_address": None,
    "billing_address": None,
    "parcels": [
        {
            "id": ANY,
            "weight": 1.0,
            "width": 42.0,
            "height": 32.0,
            "length": 32.0,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "items": [],
            "reference_number": ANY,
            "freight_class": None,
            "options": {},
            "object_type": "parcel",
        }
    ],
    "services": ["canadapost_priority"],
    "options": {
        "insurance": 100,
        "shipping_date": ANY,
        "shipment_date": ANY,
    },
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "customs": None,
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {
                    "name": "Duty and taxes",
                    "amount": 13.92,
                    "currency": "CAD",
                    "id": None,
                },
                {
                    "name": "Fuel surcharge",
                    "amount": 2.7,
                    "currency": "CAD",
                    "id": None,
                },
                {
                    "name": "SMB Savings",
                    "amount": -11.74,
                    "currency": "CAD",
                    "id": None,
                },
                {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": None},
                {
                    "name": "Base surcharge",
                    "amount": 101.83,
                    "currency": "CAD",
                    "id": None,
                },
            ],
            "estimated_delivery": None,
            "meta": {
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "ext": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": False,
        }
    ],
    "reference": None,
    "label_type": "PDF",
    "carrier_ids": ["canadapost"],
    "tracker_id": ANY,
    "created_at": ANY,
    "metadata": {},
    "messages": [],
    "status": "purchased",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "tracking_number": "123456789012",
    "shipment_identifier": "123456789012",
    "selected_rate": {
        "id": ANY,
        "object_type": "rate",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "currency": "CAD",
        "service": "canadapost_priority",
        "total_charge": 106.71,
        "transit_days": 2,
        "extra_charges": [
            {"name": "Duty and taxes", "amount": 13.92, "currency": "CAD", "id": None},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": None},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": None},
            {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": None},
            {"name": "Base surcharge", "amount": 101.83, "currency": "CAD", "id": None},
        ],
        "estimated_delivery": None,
        "meta": {
            "carrier": "canadapost",
            "carrier_connection_id": ANY,
            "ext": "canadapost",
            "rate_provider": "canadapost",
            "service_name": "CANADAPOST PRIORITY",
        },
        "test_mode": False,
    },
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "service_name": "CANADAPOST PRIORITY",
        "rate_provider": "canadapost",
    },
    "service": "canadapost_priority",
    "selected_rate_id": ANY,
    "test_mode": False,
    "label_url": ANY,
    "invoice_url": None,
    "documents": {"invoice": None, "label": ANY},
}
