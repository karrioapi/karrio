import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.server.core.tests import APITestCase
import karrio.server.automation.models as models
import karrio.core.models as datatypes


class TestShippingEngineIntegration(APITestCase):
    """Test end-to-end shipping rules integration with shipment creation following test_shipments.py patterns."""

    def setUp(self):
        super().setUp()

        # Create a simple shipping rule that selects the cheapest rate for CA destinations
        self.us_cheapest_rule = models.ShippingRule.objects.create(
            name="Canada Cheapest Rule",
            slug="ca_cheapest_rule",
            priority=1,
            is_active=True,
            conditions={"destination": {"country_code": "CA"}},
            actions={"select_service": {"strategy": "cheapest"}},
            created_by=self.user,
        )

    def test_create_shipment_with_cheapest_rule(self):
        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_CA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [MULTI_RATE_RESPONSE_CA, CREATED_SHIPMENT_RESPONSE_CA]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, PURCHASED_SHIPMENT_CA)

    def test_us_first_class_weight_rule(self):
        """Test ShipStation-style weight threshold rule for USPS First Class under 16oz."""
        # Create weight-based rule for lightweight US packages
        models.ShippingRule.objects.create(
            name="USPS First Class Under 16oz",
            slug="usps_first_class_16oz",
            priority=1,
            is_active=True,
            conditions={
                "destination": {"country_code": "US"},
                "weight": {"max": 16, "unit": "oz"}
            },
            actions={
                "select_service": {"carrier_code": "usps", "service_code": "usps_first_class"}
            },
            created_by=self.user,
        )

        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_US_LIGHTWEIGHT

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [US_LIGHTWEIGHT_RATES_RESPONSE, CREATED_SHIPMENT_USPS_FIRST_CLASS]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["selected_rate"]["service"], "usps_first_class")

        # Verify rule metadata is present
        applied_rule = response_data["selected_rate"]["meta"]["applied_rule"]
        self.assertEqual(applied_rule["rule_name"], "USPS First Class Under 16oz")
        self.assertIn("weight:", str(applied_rule["conditions_matched"]))

    def test_canada_fastest_rule(self):
        """Test fastest service selection for heavy Canadian packages."""
        # Create fastest service rule for heavy CA packages
        models.ShippingRule.objects.create(
            name="Canada Heavy Fastest",
            slug="ca_heavy_fastest",
            priority=1,
            is_active=True,
            conditions={
                "destination": {"country_code": "CA"},
                "weight": {"min": 10, "unit": "kg"}
            },
            actions={
                "select_service": {"strategy": "fastest"}
            },
            created_by=self.user,
        )

        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_CA_HEAVY

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [CA_HEAVY_RATES_RESPONSE, CREATED_SHIPMENT_CA_EXPRESS]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should select express (1 day) over regular (5 days)
        self.assertEqual(response_data["selected_rate"]["service"], "canadapost_express")
        self.assertEqual(response_data["selected_rate"]["transit_days"], 1)

    def test_fedex_carrier_preference_rule(self):
        """Test carrier preference rule selecting FedEx for medium weight US packages."""
        # Create FedEx preference rule for medium weight US packages
        models.ShippingRule.objects.create(
            name="FedEx for Medium Weight US",
            slug="fedex_medium_us",
            priority=1,
            is_active=True,
            conditions={
                "destination": {"country_code": "US"},
                "weight": {"min": 20, "max": 100, "unit": "lb"}
            },
            actions={
                "select_service": {"carrier_code": "fedex"}
            },
            created_by=self.user,
        )

        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_US_MEDIUM_WEIGHT

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [US_MIXED_CARRIERS_RESPONSE, CREATED_SHIPMENT_FEDEX]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should select FedEx even if UPS is cheaper
        self.assertTrue(response_data["selected_rate"]["carrier_name"].startswith("fedex"))

    def test_manual_override_prevents_rules(self):
        """Test that manual rate selection overrides shipping rules."""
        url = reverse("karrio.server.manager:shipment-list")
        data = {
            **SHIPMENT_DATA_CA,
            "selected_rate_id": "manual_rate_123"  # Manual override
        }

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [MULTI_RATE_RESPONSE_CA, CREATED_SHIPMENT_RESPONSE_CA]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Manual selection should win, no rule metadata should be present
        self.assertNotIn("applied_rule", response_data["selected_rate"].get("meta", {}))

    def test_rules_disabled_no_automatic_selection(self):
        """Test that no automatic selection occurs when rules are disabled."""
        url = reverse("karrio.server.manager:shipment-list")
        data = {
            **SHIPMENT_DATA_CA,
            "options": {"apply_shipping_rules": False}  # Rules disabled
        }

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [MULTI_RATE_RESPONSE_CA, None]  # No shipment creation
            response = self.client.post(url, data)

        # Should not automatically select a rate or create shipment without manual selection
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_matching_rules_no_selection(self):
        """Test that no automatic selection occurs when no rules match."""
        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_EUROPE  # European destination, no rules defined

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [EUROPE_RATES_RESPONSE, None]  # No shipment creation
            response = self.client.post(url, data)

        # Should not automatically select a rate without matching rules
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_priority_ordering_with_blocking_rule(self):
        """Test that higher priority rules block lower priority ones."""
        # Create a blocking rule with higher priority
        models.ShippingRule.objects.create(
            name="Block CA Express",
            slug="block_ca_express",
            priority=0,  # Higher priority (lower number)
            is_active=True,
            conditions={"destination": {"country_code": "CA"}},
            actions={"block_service": {"service_code": "canadapost_express"}},
            created_by=self.user,
        )

        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_CA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [MULTI_RATE_RESPONSE_CA, CREATED_SHIPMENT_RESPONSE_CA]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should not select express service due to blocking rule
        self.assertNotEqual(response_data["selected_rate"]["service"], "canadapost_express")

    def test_activity_tracking_metadata(self):
        """Test that rule activity is properly tracked in shipment metadata."""
        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA_CA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [MULTI_RATE_RESPONSE_CA, CREATED_SHIPMENT_RESPONSE_CA]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify comprehensive rule activity tracking
        rule_activity = response_data.get("meta", {}).get("rule_activity", {})
        self.assertIn("applied_rule", rule_activity)

        applied_rule_data = rule_activity["applied_rule"]
        self.assertEqual(applied_rule_data["slug"], "ca_cheapest_rule")
        self.assertIn("timestamp", applied_rule_data)
        self.assertEqual(applied_rule_data["action"], "select_service: cheapest")

        # Verify selected rate metadata
        applied_rule = response_data["selected_rate"]["meta"]["applied_rule"]
        self.assertEqual(applied_rule["rule_name"], "Canada Cheapest Rule")
        self.assertEqual(applied_rule["priority"], 1)
        self.assertIn("conditions_matched", applied_rule)
        self.assertIn("action_taken", applied_rule)


SHIPMENT_DATA_CA = {
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
    "carrier_ids": ["canadapost"],
    "options": {"apply_shipping_rules": True},
}

MULTI_RATE_RESPONSE_CA = [
    [
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_priority",
            total_charge=25.75,
            transit_days=1,
        ),
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_regular",
            total_charge=15.50,  # Cheapest
            transit_days=5,
        ),
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_express",
            total_charge=35.00,
            transit_days=1,
        ),
    ],
    [],  # messages
]

CREATED_SHIPMENT_RESPONSE_CA = (
    datatypes.ShipmentDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        tracking_number="123456789012",
        shipment_identifier="123456789012",
        docs=dict(label="==apodifjoefr"),
    ),
    [],
)

PURCHASED_SHIPMENT_CA = {
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
            "reference_number": "123456789012",
            "freight_class": None,
            "options": {},
            "object_type": "parcel",
        }
    ],
    "services": [],
    "options": {
        "apply_shipping_rules": True,
        "shipping_date": "2025-06-04T10:00",
        "shipment_date": "2025-06-04",
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
            "service": "canadapost_regular",
            "total_charge": 15.5,
            "transit_days": 5,
            "extra_charges": [],
            "estimated_delivery": None,
            "meta": {
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "ext": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST REGULAR",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_priority",
            "total_charge": 25.75,
            "transit_days": 1,
            "extra_charges": [],
            "estimated_delivery": None,
            "meta": {
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "ext": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_express",
            "total_charge": 35.0,
            "transit_days": 1,
            "extra_charges": [],
            "estimated_delivery": None,
            "meta": {
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "ext": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST EXPRESS",
            },
            "test_mode": True,
        },
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
        "service": "canadapost_regular",
        "total_charge": 15.5,
        "transit_days": 5,
        "extra_charges": [],
        "estimated_delivery": None,
        "meta": {
            "applied_rule": {
                "action_taken": "select_service: cheapest",
                "applied_at": ANY,
                "conditions_matched": ["destination.country_code: CA"],
                "priority": 1,
                "rule_id": ANY,
                "rule_name": "Canada Cheapest Rule",
                "rule_slug": "ca_cheapest_rule",
            },
            "carrier": "canadapost",
            "carrier_connection_id": ANY,
            "ext": "canadapost",
            "rate_provider": "canadapost",
            "service_name": "CANADAPOST REGULAR",
        },
        "test_mode": True,
    },
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "service_name": "CANADAPOST REGULAR",
        "rate_provider": "canadapost",
        "rule_activity": {
            "applied_rule": {
                "id": ANY,
                "slug": "ca_cheapest_rule",
                "timestamp": ANY,
                "action": "select_service: cheapest",
            }
        },
    },
    "service": "canadapost_regular",
    "selected_rate_id": ANY,
    "test_mode": True,
    "label_url": ANY,
    "invoice_url": None,
}

# Additional test data for comprehensive testing

SHIPMENT_DATA_US_LIGHTWEIGHT = {
    "recipient": {
        "address_line1": "456 Oak Ave",
        "person_name": "Jane Smith",
        "company_name": "Test Corp",
        "phone_number": "555-123-4567",
        "city": "Los Angeles",
        "country_code": "US",
        "postal_code": "90210",
        "residential": False,
        "state_code": "CA",
    },
    "shipper": {
        "address_line1": "123 Main St",
        "person_name": "John Doe",
        "company_name": "Ship Corp",
        "phone_number": "555-987-6543",
        "city": "New York",
        "country_code": "US",
        "postal_code": "10001",
        "residential": False,
        "state_code": "NY",
    },
    "parcels": [
        {
            "weight": 0.75,  # 12oz package (under 16oz threshold)
            "weight_unit": "LB",
        }
    ],
    "payment": {"currency": "USD", "paid_by": "sender"},
    "carrier_ids": ["usps"],
    "options": {"apply_shipping_rules": True},
}

SHIPMENT_DATA_CA_HEAVY = {
    "recipient": {
        "address_line1": "789 Maple St",
        "person_name": "Bob Johnson",
        "company_name": "Heavy Corp",
        "phone_number": "416-555-0123",
        "city": "Toronto",
        "country_code": "CA",
        "postal_code": "M5V3A8",
        "residential": False,
        "state_code": "ON",
    },
    "shipper": {
        "address_line1": "321 Pine Ave",
        "person_name": "Alice Brown",
        "company_name": "Sender Corp",
        "phone_number": "604-555-9876",
        "city": "Vancouver",
        "country_code": "CA",
        "postal_code": "V6B1A1",
        "residential": False,
        "state_code": "BC",
    },
    "parcels": [
        {
            "weight": 15,  # 15kg package (over 10kg threshold)
            "weight_unit": "KG",
        }
    ],
    "payment": {"currency": "CAD", "paid_by": "sender"},
    "carrier_ids": ["canadapost"],
    "options": {"apply_shipping_rules": True},
}

SHIPMENT_DATA_US_MEDIUM_WEIGHT = {
    "recipient": {
        "address_line1": "654 Cedar Ln",
        "person_name": "Mike Wilson",
        "company_name": "Medium Corp",
        "phone_number": "312-555-2468",
        "city": "Chicago",
        "country_code": "US",
        "postal_code": "60601",
        "residential": False,
        "state_code": "IL",
    },
    "shipper": {
        "address_line1": "987 Birch St",
        "person_name": "Sarah Davis",
        "company_name": "Heavy Sender",
        "phone_number": "713-555-1357",
        "city": "Houston",
        "country_code": "US",
        "postal_code": "77001",
        "residential": False,
        "state_code": "TX",
    },
    "parcels": [
        {
            "weight": 50,  # 50lb package (within 20-100lb range)
            "weight_unit": "LB",
        }
    ],
    "payment": {"currency": "USD", "paid_by": "sender"},
    "carrier_ids": ["fedex", "ups"],
    "options": {"apply_shipping_rules": True},
}

SHIPMENT_DATA_EUROPE = {
    "recipient": {
        "address_line1": "123 European St",
        "person_name": "Hans Mueller",
        "company_name": "Euro Corp",
        "phone_number": "+49-30-12345678",
        "city": "Berlin",
        "country_code": "DE",
        "postal_code": "10115",
        "residential": False,
    },
    "shipper": {
        "address_line1": "456 US Sender Ave",
        "person_name": "American Sender",
        "company_name": "US Export Corp",
        "phone_number": "555-999-8888",
        "city": "Miami",
        "country_code": "US",
        "postal_code": "33101",
        "residential": False,
        "state_code": "FL",
    },
    "parcels": [
        {
            "weight": 2,
            "weight_unit": "KG",
        }
    ],
    "payment": {"currency": "USD", "paid_by": "sender"},
    "carrier_ids": ["dhl", "ups"],
    "options": {"apply_shipping_rules": True},
}

# Mock rate responses for test scenarios

US_LIGHTWEIGHT_RATES_RESPONSE = [
    [
        datatypes.RateDetails(
            carrier_id="usps",
            carrier_name="usps",
            currency="USD",
            service="usps_first_class",
            total_charge=3.50,  # Cheapest for lightweight
            transit_days=3,
        ),
        datatypes.RateDetails(
            carrier_id="usps",
            carrier_name="usps",
            currency="USD",
            service="usps_priority",
            total_charge=8.75,
            transit_days=2,
        ),
    ],
    [],  # messages
]

CA_HEAVY_RATES_RESPONSE = [
    [
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_express",
            total_charge=45.00,
            transit_days=1,  # Fastest
        ),
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_priority",
            total_charge=35.00,
            transit_days=2,
        ),
        datatypes.RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            service="canadapost_regular",
            total_charge=25.00,  # Cheapest but slowest
            transit_days=5,
        ),
    ],
    [],  # messages
]

US_MIXED_CARRIERS_RESPONSE = [
    [
        datatypes.RateDetails(
            carrier_id="ups",
            carrier_name="ups",
            currency="USD",
            service="ups_ground",
            total_charge=35.00,  # Cheaper than FedEx
            transit_days=3,
        ),
        datatypes.RateDetails(
            carrier_id="fedex",
            carrier_name="fedex",
            currency="USD",
            service="fedex_ground",
            total_charge=42.00,  # More expensive but preferred
            transit_days=3,
        ),
    ],
    [],  # messages
]

EUROPE_RATES_RESPONSE = [
    [
        datatypes.RateDetails(
            carrier_id="dhl",
            carrier_name="dhl",
            currency="USD",
            service="dhl_express",
            total_charge=85.00,
            transit_days=2,
        ),
        datatypes.RateDetails(
            carrier_id="ups",
            carrier_name="ups",
            currency="USD",
            service="ups_worldwide_express",
            total_charge=95.00,
            transit_days=2,
        ),
    ],
    [],  # messages
]

# Mock created shipment responses

CREATED_SHIPMENT_USPS_FIRST_CLASS = (
    datatypes.ShipmentDetails(
        carrier_id="usps",
        carrier_name="usps",
        tracking_number="9400111699000123456789",
        shipment_identifier="9400111699000123456789",
        docs=dict(label="==usps_first_class_label"),
    ),
    [],
)

CREATED_SHIPMENT_CA_EXPRESS = (
    datatypes.ShipmentDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        tracking_number="123456789013",
        shipment_identifier="123456789013",
        docs=dict(label="==ca_express_label"),
    ),
    [],
)

CREATED_SHIPMENT_FEDEX = (
    datatypes.ShipmentDetails(
        carrier_id="fedex",
        carrier_name="fedex",
        tracking_number="794612345678",
        shipment_identifier="794612345678",
        docs=dict(label="==fedex_label"),
    ),
    [],
)
