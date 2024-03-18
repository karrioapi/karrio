import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import PickupDetails, ConfirmationDetails, ChargeDetails
from karrio.server.core.tests import APITestCase


class TesPickup(APITestCase):
    def test_schedule_pickup(self):
        url = reverse(
            "karrio.server.proxy:pickup-schedule",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, PICKUP_RESPONSE)

    def test_udpate_pickup(self):
        url = reverse(
            "karrio.server.proxy:pickup-details",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = UPDATE_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_UPDATE_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_UPDATE_RESPONSE)

    def test_cancel_pickup(self):
        url = reverse(
            "karrio.server.proxy:pickup-cancel",
            kwargs=dict(carrier_name="canadapost"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CANCEL_RETURNED_VALUE
            response = self.client.post(f"{url}", PICKUP_CANCEL_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_CANCEL_RESPONSE)


PICKUP_DATA = {
    "pickup_date": "2020-10-25",
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
    "parcels": [
        {
            "weight": 0.2,
            "width": 10,
            "height": 10,
            "length": 1,
            "packaging_type": "envelope",
            "is_document": True,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "ready_time": "13:00",
    "closing_time": "17:00",
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
}

PICKUP_UPDATE_DATA = {
    "pickup_date": "2020-10-23",
    "confirmation_number": "27241",
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
    "parcels": [
        {
            "weight": 0.2,
            "width": 10,
            "height": 10,
            "length": 1,
            "packaging_type": "envelope",
            "is_document": True,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "ready_time": "14:30",
    "closing_time": "17:00",
    "instruction": "Should not be folded",
    "package_location": "At the main entrance hall",
}

PICKUP_CANCEL_DATA = {"confirmation_number": "00110215"}


SCHEDULE_RETURNED_VALUE = (
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
)

UPDATE_RETURNED_VALUE = (
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-23",
        ready_time="14:30",
        closing_time="17:00",
    ),
    [],
)

CANCEL_RETURNED_VALUE = (
    ConfirmationDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        operation="Cancel Pickup",
        success=True,
    ),
    [],
)


PICKUP_RESPONSE = {
    "messages": [],
    "pickup": {
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
            "id": None,
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
            "address_line2": "",
            "validate_location": False,
            "validation": None,
        },
        "parcels": [
            {
                "id": None,
                "object_type": "parcel",
                "weight": 0.2,
                "width": 10.0,
                "height": 10.0,
                "length": 1.0,
                "packaging_type": "envelope",
                "package_preset": None,
                "description": None,
                "content": None,
                "is_document": True,
                "items": [],
                "weight_unit": "KG",
                "dimension_unit": "CM",
                "freight_class": None,
                "reference_number": None,
                "options": {},
            }
        ],
        "instruction": "Should not be folded",
        "package_location": "At the main entrance hall",
        "options": {},
        "metadata": {},
        "meta": {"ext": "canadapost"},
    },
}

PICKUP_UPDATE_RESPONSE = {
    "messages": [],
    "pickup": {
        "id": None,
        "object_type": "pickup",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "confirmation_number": "27241",
        "pickup_date": "2020-10-23",
        "pickup_charge": None,
        "ready_time": "14:30",
        "closing_time": "17:00",
        "test_mode": True,
        "address": {
            "id": None,
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
            "address_line2": "",
            "validate_location": False,
            "validation": None,
        },
        "parcels": [
            {
                "id": None,
                "object_type": "parcel",
                "weight": 0.2,
                "width": 10.0,
                "height": 10.0,
                "length": 1.0,
                "packaging_type": "envelope",
                "package_preset": None,
                "description": None,
                "content": None,
                "is_document": True,
                "items": [],
                "weight_unit": "KG",
                "dimension_unit": "CM",
                "freight_class": None,
                "reference_number": None,
                "options": {},
            }
        ],
        "instruction": "Should not be folded",
        "package_location": "At the main entrance hall",
        "options": {},
        "metadata": {},
        "meta": {},
    },
}

PICKUP_CANCEL_RESPONSE = {
    "messages": [],
    "confirmation": {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "operation": "Cancel Pickup",
        "success": True,
    },
}
