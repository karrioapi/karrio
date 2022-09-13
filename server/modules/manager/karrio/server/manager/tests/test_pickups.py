import json
import logging
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import PickupDetails, ConfirmationDetails, ChargeDetails
from karrio.server.manager.tests.test_shipments import TestShipmentFixture
import karrio.server.manager.models as models


class TestFixture(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()

        self.address: models.Address = models.Address.objects.create(
            **{
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
                "suburb": None,
                "residential": False,
                "address_line1": "125 Church St",
                "address_line2": None,
                "validate_location": False,
                "validation": None,
                "created_by": self.user,
            }
        )
        self.shipment.tracking_number = "123456789012"
        self.shipment.selected_rate_carrier = self.carrier
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


class TestPickupDetails(TestFixture):
    def setUp(self) -> None:
        super().setUp()
        self.pickup: models.Pickup = models.Pickup.objects.create(
            address=self.address,
            pickup_carrier=self.carrier,
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
    "pickup_charge": {"name": "Pickup fees", "amount": 0.0, "currency": "CAD"},
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
        "suburb": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
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
        }
    ],
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
    "options": {},
    "metadata": {},
}

PICKUP_UPDATE_RESPONSE = {
    "id": ANY,
    "object_type": "pickup",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "confirmation_number": "00110215",
    "pickup_date": "2020-10-25",
    "pickup_charge": {"name": "Pickup fees", "amount": 0.0, "currency": "CAD"},
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
        "suburb": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
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
        }
    ],
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall next to the distributor",
    "options": {},
    "metadata": {},
}

PICKUP_CANCEL_RESPONSE = {
    "id": ANY,
    "object_type": "pickup",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "confirmation_number": "00110215",
    "pickup_date": "2020-10-25",
    "pickup_charge": {"name": "Pickup fees", "amount": 0.0, "currency": "CAD"},
    "ready_time": "13:00",
    "closing_time": "17:00",
    "address": {
        "id": None,
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
        "suburb": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "parcels": [
        {
            "id": ANY,
            "weight": 1.0,
            "width": None,
            "height": None,
            "length": None,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "weight_unit": "KG",
            "dimension_unit": None,
            "items": [],
            "freight_class": None,
            "reference_number": "0000000002",
            "options": {},
            "object_type": "parcel",
        }
    ],
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
    "options": {},
    "metadata": {},
    "test_mode": True,
}
