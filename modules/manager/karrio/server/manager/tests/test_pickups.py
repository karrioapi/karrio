import json
import logging
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import PickupDetails, ConfirmationDetails, ChargeDetails
from karrio.server.manager.tests.test_shipments import TestShipmentFixture
from karrio.server.core.utils import create_carrier_snapshot
import karrio.server.manager.models as models


class TestFixture(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()

        # Address as dict data for JSON field (use proper JSON-generated ID format)
        self.address_data = {
            "id": "adr_001122334455",
            "postal_code": "E1C4Z8",
            "city": "Moncton",
            "federal_tax_id": None,
            "state_tax_id": None,
            "person_name": "John Poop",
            "company_name": "A corp.",
            "country_code": "CA",
            "email": "john@a.com",
            "phone_number": "514 000 0000",
            "state_code": "NB",
            "street_number": None,
            "residential": False,
            "address_line1": "125 Church St",
            "address_line2": None,
            "validate_location": False,
            "validation": None,
        }
        self.shipment.tracking_number = "123456789012"
        # Set selected_rate and carrier snapshot
        self.shipment.selected_rate = {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "service": "canadapost_priority",
        }
        self.shipment.carrier = create_carrier_snapshot(self.carrier)
        self.shipment.save()


class TestPickupSchedule(TestFixture):
    def test_schedule_pickup(self):
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, PICKUP_RESPONSE)

    def test_schedule_pickup_with_parcels_count(self):
        """Test scheduling a standalone pickup using parcels_count instead of tracking_numbers."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA_STANDALONE)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response_data["confirmation_number"], "27241")

    def test_schedule_pickup_validation_no_source(self):
        """Test that validation fails when neither tracking_numbers nor parcels_count is provided."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        response = self.client.post(f"{url}", PICKUP_DATA_NO_SOURCE)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("errors", response_data)

    def test_schedule_pickup_validation_standalone_no_address(self):
        """Test that validation fails for standalone pickup without address."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        response = self.client.post(f"{url}", PICKUP_DATA_STANDALONE_NO_ADDRESS)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("errors", response_data)

    def test_backward_compatibility_tracking_numbers(self):
        """Test that the existing tracking_numbers flow still works."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_schedule_pickup_with_pickup_type_one_time(self):
        """Test scheduling a pickup with explicit one_time pickup_type."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA_ONE_TIME)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response_data["pickup_type"], "one_time")
            self.assertIsNone(response_data["recurrence"])

    def test_schedule_pickup_with_pickup_type_daily(self):
        """Test scheduling a pickup with daily pickup_type."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA_DAILY)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response_data["pickup_type"], "daily")

    def test_schedule_pickup_with_pickup_type_recurring(self):
        """Test scheduling a pickup with recurring pickup_type and recurrence config."""
        url = reverse(
            "karrio.server.manager:shipment-pickup-request",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA_RECURRING)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response_data["pickup_type"], "recurring")
            self.assertIsNotNone(response_data["recurrence"])
            self.assertEqual(response_data["recurrence"]["frequency"], "weekly")
            self.assertIn("monday", response_data["recurrence"]["days_of_week"])


class TestPickupDetails(TestFixture):
    def setUp(self) -> None:
        super().setUp()
        self.pickup: models.Pickup = models.Pickup.objects.create(
            address=self.address_data,
            carrier=create_carrier_snapshot(self.carrier),
            created_by=self.user,
            test_mode=True,
            pickup_date="2020-10-25",
            ready_time="13:00",
            closing_time="17:00",
            instruction="Should not be folded",
            package_location="At the main entrance hall",
            confirmation_number="00110215",
            pickup_charge={"name": "Pickup fees", "amount": 0.0, "currency": "CAD"},
        )
        self.pickup.shipments.set([self.shipment])

    def test_udpate_pickup(self):
        url = reverse(
            "karrio.server.manager:shipment-pickup-details",
            kwargs=dict(pk=self.pickup.pk),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = UPDATE_RETURNED_VALUE
            response = self.client.post(url, PICKUP_UPDATE_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_UPDATE_RESPONSE)

    def test_cancel_pickup(self):
        url = reverse(
            "karrio.server.manager:shipment-pickup-cancel",
            kwargs=dict(pk=self.pickup.pk),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CANCEL_RETURNED_VALUE
            response = self.client.post(url, {})
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_CANCEL_RESPONSE)


PICKUP_DATA = {
    "pickup_date": "2020-10-25",
    "ready_time": "13:00",
    "closing_time": "17:00",
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
    "address": {
        "id": "adr_aabbccddeeff",  # JSON-generated ID format
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "email": "john@a.com",
        "validate_location": False,
        "validation": None,
    },
    "tracking_numbers": ["123456789012"],
}

# Test data for standalone pickup with parcels_count
PICKUP_DATA_STANDALONE = {
    "pickup_date": "2020-10-25",
    "ready_time": "13:00",
    "closing_time": "17:00",
    "instruction": "Handle with care",
    "package_location": "Front desk",
    "address": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "email": "john@a.com",
    },
    "parcels_count": 3,
}

# Test data with neither tracking_numbers nor parcels_count (should fail validation)
PICKUP_DATA_NO_SOURCE = {
    "pickup_date": "2020-10-25",
    "ready_time": "13:00",
    "closing_time": "17:00",
    "address": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
    },
}

# Test data for standalone pickup without address (should fail validation)
PICKUP_DATA_STANDALONE_NO_ADDRESS = {
    "pickup_date": "2020-10-25",
    "ready_time": "13:00",
    "closing_time": "17:00",
    "parcels_count": 2,
}

# Test data for pickup with explicit one_time pickup_type
PICKUP_DATA_ONE_TIME = {
    "pickup_date": "2020-10-25",
    "ready_time": "13:00",
    "closing_time": "17:00",
    "instruction": "One-time pickup",
    "package_location": "Front door",
    "address": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "email": "john@a.com",
    },
    "tracking_numbers": ["123456789012"],
    "pickup_type": "one_time",
}

# Test data for daily pickup
PICKUP_DATA_DAILY = {
    "pickup_date": "2020-10-25",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Daily pickup",
    "package_location": "Loading dock",
    "address": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "email": "john@a.com",
    },
    "tracking_numbers": ["123456789012"],
    "pickup_type": "daily",
}

# Test data for recurring pickup
PICKUP_DATA_RECURRING = {
    "pickup_date": "2020-10-25",
    "ready_time": "10:00",
    "closing_time": "16:00",
    "instruction": "Weekly recurring pickup",
    "package_location": "Warehouse bay 3",
    "address": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "email": "john@a.com",
    },
    "tracking_numbers": ["123456789012"],
    "pickup_type": "recurring",
    "recurrence": {
        "frequency": "weekly",
        "days_of_week": ["monday", "wednesday", "friday"],
    },
}

PICKUP_UPDATE_DATA = {
    "ready_time": "14:00",
    "package_location": "At the main entrance hall next to the distributor",
    "address": {"person_name": "Janet Jackson"},
}


SCHEDULE_RETURNED_VALUE = [
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-25",
        pickup_charge=ChargeDetails(name="Pickup fees", amount=0.0, currency="CAD"),
        ready_time="13:00",
        closing_time="17:00",
    ),
    [],
]

UPDATE_RETURNED_VALUE = [
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-23",
        ready_time="14:00",
        closing_time="17:00",
    ),
    [],
]

CANCEL_RETURNED_VALUE = [
    ConfirmationDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        operation="Cancel Pickup",
        success=True,
    ),
    [],
]


PICKUP_RESPONSE = {
    "id": ANY,
    "object_type": "pickup",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "confirmation_number": "27241",
    "pickup_date": "2020-10-25",
    "pickup_charge": {
        "name": "Pickup fees",
        "amount": 0.0,
        "currency": "CAD",
        "id": ANY,
    },
    "ready_time": "13:00",
    "closing_time": "17:00",
    "test_mode": True,
    "address": {
        "id": ANY,
        "object_type": "address",
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Doe",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": "john@a.com",
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
        "meta": {},
    },
    "parcels": [
        {
            "id": ANY,
            "object_type": "parcel",
            "weight": 1.0,
            "width": None,
            "height": None,
            "length": None,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "items": [],
            "weight_unit": "KG",
            "dimension_unit": None,
            "freight_class": None,
            "reference_number": ANY,
            "options": {},
            "meta": {},
        }
    ],
    "parcels_count": None,
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
    "pickup_type": "one_time",
    "recurrence": None,
    "options": {},
    "metadata": {},
    "meta": ANY,
}

PICKUP_UPDATE_RESPONSE = {
    "id": ANY,
    "object_type": "pickup",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "confirmation_number": "00110215",
    "pickup_date": "2020-10-25",
    "pickup_charge": {
        "name": "Pickup fees",
        "amount": 0.0,
        "currency": "CAD",
        "id": ANY,
    },
    "ready_time": "14:00",
    "closing_time": "17:00",
    "test_mode": True,
    "address": {
        "id": ANY,
        "object_type": "address",
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Janet Jackson",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": "john@a.com",
        "phone_number": "514 000 0000",
        "state_code": "NB",
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
        "meta": {},
    },
    "parcels": [
        {
            "id": ANY,
            "object_type": "parcel",
            "weight": 1.0,
            "width": None,
            "height": None,
            "length": None,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "items": [],
            "weight_unit": "KG",
            "dimension_unit": None,
            "freight_class": None,
            "reference_number": ANY,
            "options": {},
            "meta": {},
        }
    ],
    "parcels_count": None,
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall next to the distributor",
    "pickup_type": "one_time",
    "recurrence": None,
    "options": {},
    "metadata": {},
    "meta": ANY,
}

PICKUP_CANCEL_RESPONSE = {
    "id": None,  # Deleted pickup has no id
    "object_type": "pickup",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "confirmation_number": "00110215",
    "pickup_date": "2020-10-25",
    "pickup_charge": {
        "name": "Pickup fees",
        "amount": 0.0,
        "currency": "CAD",
        "id": None,
    },
    "ready_time": "13:00",
    "closing_time": "17:00",
    "address": {
        "id": "adr_001122334455",  # JSON address retains its id
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": "john@a.com",
        "phone_number": "514 000 0000",
        "state_code": "NB",
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "parcels": [],  # Deleted pickup has no parcels
    "parcels_count": None,
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
    "pickup_type": "one_time",
    "recurrence": None,
    "options": {},
    "metadata": {},
    "test_mode": True,
    "meta": ANY,
}
