import json
from unittest.mock import ANY, patch
from django.urls import reverse
from rest_framework import status
from karrio.core.models import RateDetails, ChargeDetails
from karrio.server.graph.tests.base import GraphTestCase, Result
import karrio.server.manager.models as manager


class TestPartialShipmentMutation(GraphTestCase):
    def setUp(self) -> None:
        super().setUp()
        # Create a draft shipment using the REST API
        self.shipment = self._create_draft_shipment()

    def _create_draft_shipment(self):
        """Create a draft shipment using the REST API without service (no rates fetched)"""
        url = reverse("karrio.server.manager:shipment-list")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, DRAFT_SHIPMENT_DATA)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = json.loads(response.content)
            return response_data

    def test_partial_update_options_with_none_values(self):
        """Test updating options with explicit None values to remove existing options"""
        shipment_id = self.shipment["id"]

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  options
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "options": {
                        "insurance": None,
                        "signature_confirmation": None,
                        "currency": "USD",
                        "new_option": "test_value",
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, OPTIONS_UPDATE_RESPONSE)

    def test_partial_update_shipper_address_fields(self):
        """Test updating random fields within shipper address"""
        shipment_id = self.shipment["id"]

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  shipper {
                    id
                    company_name
                    person_name
                    phone_number
                    email
                    city
                    postal_code
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "shipper": {
                        "company_name": "Updated Corp Inc.",
                        "email": "updated@example.com",
                        "phone_number": "555-123-4567",
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, SHIPPER_UPDATE_RESPONSE)

    def test_partial_update_recipient_address_fields(self):
        """Test updating random fields within recipient address"""
        shipment_id = self.shipment["id"]

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  recipient {
                    id
                    company_name
                    person_name
                    address_line1
                    city
                    state_code
                    residential
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "recipient": {
                        "person_name": "John Updated",
                        "address_line1": "456 Updated St",
                        "residential": True,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, RECIPIENT_UPDATE_RESPONSE)

    def test_partial_update_payment_and_metadata(self):
        """Test updating payment information and metadata"""
        shipment_id = self.shipment["id"]

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  payment {
                    paid_by
                    currency
                    account_number
                  }
                  metadata
                  reference
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "payment": {"paid_by": "recipient", "account_number": "123456789"},
                    "metadata": {"customer_id": "CUST123", "order_number": "ORD456"},
                    "reference": "REF789",
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PAYMENT_METADATA_UPDATE_RESPONSE)

    def test_partial_update_parcel_information(self):
        """Test updating parcel information"""
        shipment_id = self.shipment["id"]

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  parcels {
                    id
                    weight
                    weight_unit
                    package_preset
                    description
                    reference_number
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "parcels": [
                        {
                            "weight": 2.5,
                            "weight_unit": "LB",
                            "description": "Updated parcel description",
                            "package_preset": "canadapost_corrugated_medium_box",
                        }
                    ],
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, PARCEL_UPDATE_RESPONSE)

    def test_partial_update_label_type_and_options_merge(self):
        """Test updating label type and ensuring options are properly merged"""
        shipment_id = self.shipment["id"]

        # First, set some initial options
        self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  options
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "options": {
                        "insurance": 100,
                        "signature_confirmation": True,
                        "currency": "CAD",
                    },
                }
            },
        )

        # Now update label type and add more options
        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  label_type
                  options
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables={
                "data": {
                    "id": shipment_id,
                    "label_type": "ZPL",
                    "options": {"delivery_confirmation": True, "priority": "high"},
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, LABEL_OPTIONS_MERGE_RESPONSE)

    def test_full_shipment_update_simulation(self):
        """Test updating multiple fields at once to simulate frontend save operation"""
        shipment_id = self.shipment["id"]

        # Set the shipment ID dynamically in the test data
        full_update_data = FULL_UPDATE_DATA.copy()
        full_update_data["data"]["id"] = shipment_id

        response = self.query(
            """
            mutation partial_shipment_update($data: PartialShipmentMutationInput!) {
              partial_shipment_update(input: $data) {
                shipment {
                  id
                  status
                  shipper {
                    company_name
                    person_name
                    email
                  }
                  recipient {
                    company_name
                    person_name
                    email
                  }
                  parcels {
                    weight
                    weight_unit
                    description
                  }
                  payment {
                    paid_by
                    currency
                  }
                  options
                  metadata
                  reference
                  label_type
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="partial_shipment_update",
            variables=full_update_data,
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, FULL_UPDATE_SIMULATION_RESPONSE)


# Test data
DRAFT_SHIPMENT_DATA = {
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
    # Note: No service specified, so this creates a draft without rates
}

RETURNED_RATES_VALUE = [
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            total_charge=106.71,
            extra_charges=[
                ChargeDetails(amount=13.92, currency="CAD", name="Duty and taxes"),
                ChargeDetails(amount=2.7, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-11.74, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=-9.04, currency="CAD", name="Discount"),
                ChargeDetails(amount=101.83, currency="CAD", name="Base surcharge"),
            ],
        )
    ],
    [],
]

FULL_UPDATE_DATA = {
    "data": {
        "id": None,  # Will be set dynamically in the test
        "shipper": {
            "company_name": "Full Update Shipper Corp",
            "person_name": "Updated Shipper",
            "email": "shipper@fullupdate.com",
        },
        "recipient": {
            "company_name": "Full Update Recipient Corp",
            "person_name": "Updated Recipient",
            "email": "recipient@fullupdate.com",
        },
        "parcels": [
            {"weight": 3.0, "weight_unit": "KG", "description": "Full update parcel"}
        ],
        "payment": {"paid_by": "third_party", "currency": "USD"},
        "options": {"insurance": 250, "priority": "express"},
        "metadata": {"full_update": True, "test_case": "full_update_simulation"},
        "reference": "FULL_UPDATE_REF",
        "label_type": "PNG",
    }
}

# Expected responses for assertDictEqual
OPTIONS_UPDATE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "options": {
                    "shipping_date": ANY,
                    "shipment_date": ANY,
                    "currency": "USD",
                    "new_option": "test_value",
                },
            },
            "errors": None,
        }
    }
}

SHIPPER_UPDATE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "shipper": {
                    "id": ANY,
                    "company_name": "Updated Corp Inc.",
                    "person_name": "Jane Doe",
                    "phone_number": "555-123-4567",
                    "email": "updated@example.com",
                    "city": "Vancouver",
                    "postal_code": "V6M2V9",
                },
            },
            "errors": None,
        }
    }
}

RECIPIENT_UPDATE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "recipient": {
                    "id": ANY,
                    "company_name": "A corp.",
                    "person_name": "John Updated",
                    "address_line1": "456 Updated St",
                    "city": "Moncton",
                    "state_code": "NB",
                    "residential": True,
                },
            },
            "errors": None,
        }
    }
}

PAYMENT_METADATA_UPDATE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "payment": {
                    "paid_by": "recipient",
                    "currency": None,
                    "account_number": "123456789",
                },
                "metadata": {
                    "customer_id": "CUST123",
                    "order_number": "ORD456",
                },
                "reference": "REF789",
            },
            "errors": None,
        }
    }
}

PARCEL_UPDATE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "parcels": [
                    {
                        "id": ANY,
                        "weight": 1.0,
                        "weight_unit": "KG",
                        "package_preset": "canadapost_corrugated_small_box",
                        "description": None,
                        "reference_number": ANY,
                    },
                    {
                        "id": ANY,
                        "weight": 2.5,
                        "weight_unit": "LB",
                        "package_preset": "canadapost_corrugated_medium_box",
                        "description": "Updated parcel description",
                        "reference_number": ANY,
                    },
                ],
            },
            "errors": None,
        }
    }
}

LABEL_OPTIONS_MERGE_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "label_type": "ZPL",
                "options": {
                    "shipping_date": ANY,
                    "shipment_date": ANY,
                    "currency": "CAD",
                    "insurance": 100,
                    "signature_confirmation": True,
                    "delivery_confirmation": True,
                    "priority": "high",
                },
            },
            "errors": None,
        }
    }
}

FULL_UPDATE_SIMULATION_RESPONSE = {
    "data": {
        "partial_shipment_update": {
            "shipment": {
                "id": ANY,
                "status": "draft",
                "shipper": {
                    "company_name": "Full Update Shipper Corp",
                    "person_name": "Updated Shipper",
                    "email": "shipper@fullupdate.com",
                },
                "recipient": {
                    "company_name": "Full Update Recipient Corp",
                    "person_name": "Updated Recipient",
                    "email": "recipient@fullupdate.com",
                },
                "parcels": [
                    {
                        "weight": 1.0,
                        "weight_unit": "KG",
                        "description": None,
                    },
                    {
                        "weight": 3.0,
                        "weight_unit": "KG",
                        "description": "Full update parcel",
                    },
                ],
                "payment": {
                    "paid_by": "third_party",
                    "currency": "USD",
                },
                "options": {
                    "shipping_date": ANY,
                    "shipment_date": ANY,
                    "insurance": 250,
                    "priority": "express",
                },
                "metadata": {
                    "full_update": True,
                    "test_case": "full_update_simulation",
                },
                "reference": "FULL_UPDATE_REF",
                "label_type": "PNG",
            },
            "errors": None,
        }
    }
}
