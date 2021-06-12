import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import ShipmentDetails, ConfirmationDetails, Message
from purpleserver.core.tests import APITestCase


class TestShipping(APITestCase):
    def test_shipping_request(self):
        url = reverse("purpleserver.proxy:shipping-request")
        data = SHIPPING_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, SHIPPING_RESPONSE)

    def test_shipping_cancel(self):
        url = reverse(
            "purpleserver.proxy:shipping-cancel", kwargs=dict(carrier_name="canadapost")
        )
        data = SHIPPING_CANCEL_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_SUCCESS_CANCEL_VALUE
            response = self.client.post(f"{url}?test", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertDictEqual(response_data, SHIPPING_CANCEL_SUCCESS_RESPONSE)

    def test_shipping_failed_cancel(self):
        url = reverse(
            "purpleserver.proxy:shipping-cancel", kwargs=dict(carrier_name="canadapost")
        )
        data = SHIPPING_CANCEL_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_FAILED_CANCEL_VALUE
            response = self.client.post(f"{url}?test", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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
        "postal_code": "V6M2V9",
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

RETURNED_VALUE = (
    ShipmentDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        label="==apodifjoefr",
        tracking_number="123456789012",
        shipment_identifier="123456789012",
    ),
    [],
)

RETURNED_SUCCESS_CANCEL_VALUE = (
    ConfirmationDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        success=True,
        operation="Cancel Shipment",
    ),
    [],
)

RETURNED_FAILED_CANCEL_VALUE = (
    None,
    [
        Message(
            carrier_name="canadapost",
            carrier_id="canadapost",
            message="Not Found",
            code="404",
        )
    ],
)

SHIPPING_RESPONSE = {
    "id": ANY,
    "status": "purchased",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "label": "==apodifjoefr",
    "label_type": "PDF",
    "tracking_number": "123456789012",
    "shipment_identifier": "123456789012",
    "selected_rate": {
        "id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "currency": "CAD",
        "service": "canadapost_priority",
        "discount": -9.04,
        "base_charge": 101.83,
        "total_charge": 106.71,
        "duties_and_taxes": 13.92,
        "transit_days": None,
        "extra_charges": [
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
        ],
        "meta": {"carrier_name": "canadapost", "service_name": "CANADAPOST PRIORITY"},
        "carrier_ref": None,
        "test_mode": True,
    },
    "selected_rate_id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
    "rates": [
        {
            "id": "prx_a9b96e5a82f644b0921bfed3190b4d6c",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_priority",
            "discount": -9.04,
            "base_charge": 101.83,
            "total_charge": 106.71,
            "duties_and_taxes": 13.92,
            "transit_days": None,
            "extra_charges": [
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
            ],
            "meta": None,
            "carrier_ref": None,
            "test_mode": True,
        },
        {
            "id": "prx_9290e4a2c8e34c8d8c73ab990b029f3d",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "service": "canadapost_regular_parcel",
            "discount": -3.06,
            "base_charge": 27.36,
            "total_charge": 27.95,
            "duties_and_taxes": 3.65,
            "transit_days": None,
            "extra_charges": [
                {"name": "Fuel surcharge", "amount": 0.71, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -3.77, "currency": "CAD"},
            ],
            "meta": None,
            "carrier_ref": None,
            "test_mode": True,
        },
    ],
    "tracking_url": "/v1/proxy/tracking/canadapost/123456789012?test",
    "service": "canadapost_priority",
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
        "phone_number": "514 000 0000",
        "state_code": "BC",
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": "",
        "validate_location": False,
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
        "phone_number": "514 000 0000",
        "state_code": "NB",
        "suburb": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": "",
        "validate_location": False,
        "validation": None,
    },
    "parcels": [
        {
            "id": None,
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
        }
    ],
    "services": [],
    "options": {},
    "payment": {"account_number": None, "currency": "CAD", "paid_by": "sender"},
    "customs": None,
    "reference": "",
    "carrier_ids": [],
    "meta": {"carrier_name": "canadapost", "service_name": "CANADAPOST PRIORITY"},
    "created_at": ANY,
    "test_mode": True,
    "messages": [],
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
    "error": {
        "code": "failure",
        "details": {
            "messages": [
                {
                    "carrier_id": "canadapost",
                    "carrier_name": "canadapost",
                    "code": "404",
                    "message": "Not Found",
                }
            ]
        },
    }
}
