import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import ShipmentDetails, ConfirmationDetails, Message
from karrio.server.core.tests import APITestCase


class TestShipping(APITestCase):
    def test_shipping_request(self):
        url = reverse("karrio.server.proxy:shipping-request")
        data = SHIPPING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, SHIPPING_RESPONSE)

    def test_shipping_cancel(self):
        url = reverse(
            "karrio.server.proxy:shipping-cancel",
            kwargs=dict(carrier_name="canadapost"),
        )
        data = SHIPPING_CANCEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_SUCCESS_CANCEL_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertDictEqual(response_data, SHIPPING_CANCEL_SUCCESS_RESPONSE)

    def test_shipping_failed_cancel(self):
        url = reverse(
            "karrio.server.proxy:shipping-cancel",
            kwargs=dict(carrier_name="canadapost"),
        )
        data = SHIPPING_CANCEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_FAILED_CANCEL_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_424_FAILED_DEPENDENCY)
            self.assertDictEqual(response_data, SHIPPING_CANCEL_FAILED_RESPONSE)


SHIPPING_DATA = {
    "selected_rate_id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
    "options": {},
    "recipient": {
        "address_line1": "125 Church St",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "phone_number": "514 000 0000",
        "city": "Moncton",
        "country_code": "CA",
        "postal_code": "E1C4Z8",
        "residential": False,
        "state_code": "NB",
        "validate_location": False,
        "validation": None,
    },
    "shipper": {
        "address_line1": "5840 Oak St",
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "phone_number": "514 000 0000",
        "city": "Vancouver",
        "country_code": "CA",
        "postal_code": "v6m2V9",
        "residential": False,
        "state_code": "BC",
        "validate_location": False,
        "validation": None,
    },
    "parcels": [
        {
            "weight": 1,
            "weight_unit": "KG",
            "package_preset": "canadapost_corrugated_small_box",
        }
    ],
    "rates": [
        {
            "base_charge": 101.83,
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "discount": -9.04,
            "duties_and_taxes": 13.92,
            "estimated_delivery": "2020-06-22",
            "extra_charges": [
                {"amount": 2.7, "currency": "CAD", "name": "Fuel surcharge"},
                {"amount": -11.74, "currency": "CAD", "name": "SMB Savings"},
            ],
            "id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "test_mode": True,
        },
        {
            "base_charge": 27.36,
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "estimated_delivery": None,
            "discount": -3.06,
            "duties_and_taxes": 3.65,
            "estimated_delivery": "2020-07-02",
            "extra_charges": [
                {"amount": 0.71, "currency": "CAD", "name": "Fuel surcharge"},
                {"amount": -3.77, "currency": "CAD", "name": "SMB Savings"},
            ],
            "id": "prx_9290e4a2c8e34c8d8c73ab990b029f3d",
            "service": "canadapost_regular_parcel",
            "total_charge": 27.95,
            "test_mode": True,
        },
    ],
    "payment": {"currency": "CAD", "paid_by": "sender"},
}

SHIPPING_CANCEL_DATA = {"shipment_identifier": "123456789012"}

RETURNED_VALUE = [
    ShipmentDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        tracking_number="123456789012",
        shipment_identifier="123456789012",
        docs=dict(label="==apodifjoefr"),
    ),
    [],
]

RETURNED_SUCCESS_CANCEL_VALUE = [
    ConfirmationDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        success=True,
        operation="Cancel Shipment",
    ),
    [],
]

RETURNED_FAILED_CANCEL_VALUE = [
    None,
    [
        Message(
            carrier_name="canadapost",
            carrier_id="canadapost",
            message="Not Found",
            code="404",
        )
    ],
]

SHIPPING_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": "/v1/proxy/tracking/canadapost/123456789012",
    "shipper": {
        "id": None,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-0000",
        "state_code": "BC",
        "street_number": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": "",
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "recipient": {
        "id": None,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Doe",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": "",
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "parcels": [
        {
            "id": None,
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
            "freight_class": None,
            "reference_number": "123456789012",
            "object_type": "parcel",
            "options": {},
        }
    ],
    "services": [],
    "options": {"shipment_date": ANY, "shipping_date": ANY},
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "billing_address": None,
    "customs": None,
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": None,
            "extra_charges": [
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
            ],
            "meta": None,
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_regular_parcel",
            "total_charge": 27.95,
            "transit_days": None,
            "extra_charges": [
                {"name": "Fuel surcharge", "amount": 0.71, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -3.77, "currency": "CAD"},
            ],
            "meta": None,
            "test_mode": True,
        },
    ],
    "reference": "",
    "return_address": None,
    "label_type": "PDF",
    "carrier_ids": [],
    "tracker_id": None,
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
        "estimated_delivery": ANY,
        "service": "canadapost_priority",
        "total_charge": 106.71,
        "transit_days": None,
        "extra_charges": [
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
        ],
        "meta": {
            "ext": "canadapost",
            "carrier": "canadapost",
            "rate_provider": "canadapost",
            "service_name": "CANADAPOST PRIORITY",
        },
        "test_mode": True,
    },
    "docs": {"label": "==apodifjoefr", "invoice": None},
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "rate_provider": "canadapost",
        "service_name": "CANADAPOST PRIORITY",
    },
    "service": "canadapost_priority",
    "selected_rate_id": ANY,
    "test_mode": True,
}

SHIPPING_CANCEL_SUCCESS_RESPONSE = {
    "messages": [],
    "confirmation": {
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "operation": "Cancel Shipment",
        "success": True,
    },
}

SHIPPING_CANCEL_FAILED_RESPONSE = {
    "messages": [
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "code": "404",
            "message": "Not Found",
        }
    ]
}
