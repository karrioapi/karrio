import json
from unittest.mock import ANY, patch
from django.urls import reverse
from rest_framework import status
from karrio.core.models import (
    RateDetails,
    ChargeDetails,
    ShipmentDetails,
    ConfirmationDetails,
)
from karrio.server.core.tests import APITestCase
import karrio.server.manager.models as models


class TestShipmentFixture(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.shipper: models.Address = models.Address.objects.create(
            **{
                "postal_code": "E1C4Z8",
                "city": "Moncton",
                "federal_tax_id": None,
                "state_tax_id": None,
                "person_name": "John Poop",
                "company_name": "A corp.",
                "country_code": "CA",
                "email": None,
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
        self.recipient: models.Address = models.Address.objects.create(
            **{
                "postal_code": "V6M2V9",
                "city": "Vancouver",
                "federal_tax_id": None,
                "state_tax_id": None,
                "person_name": "Jane Doe",
                "company_name": "B corp.",
                "country_code": "CA",
                "email": None,
                "phone_number": "514 000 9999",
                "state_code": "BC",
                "suburb": None,
                "residential": False,
                "address_line1": "5840 Oak St",
                "address_line2": None,
                "validate_location": False,
                "validation": None,
                "created_by": self.user,
            }
        )
        self.parcel: models.Parcel = models.Parcel.objects.create(
            **{
                "weight": 1.0,
                "weight_unit": "KG",
                "package_preset": "canadapost_corrugated_small_box",
                "created_by": self.user,
            }
        )
        self.shipment: models.Shipment = models.Shipment.objects.create(
            shipper=self.shipper,
            recipient=self.recipient,
            created_by=self.user,
            test_mode=True,
            payment={"currency": "CAD", "paid_by": "sender"},
        )
        self.shipment.parcels.set([self.parcel])


class TestShipments(APITestCase):
    def test_create_shipment(self):
        url = reverse("karrio.server.manager:shipment-list")
        data = SHIPMENT_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, SHIPMENT_RESPONSE)


class TestShipmentDetails(TestShipmentFixture):
    def test_update_shipment_options(self):
        url = reverse(
            "karrio.server.manager:shipment-details",
            kwargs=dict(pk=self.shipment.pk),
        )
        data = SHIPMENT_OPTIONS

        response = self.client.put(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response_data.get("options"), SHIPMENT_OPTIONS.get("options")
        )

    def test_shipment_rates(self):
        url = reverse(
            "karrio.server.manager:shipment-rates", kwargs=dict(pk=self.shipment.pk)
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, {})
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(rates=response_data["rates"]), SHIPMENT_RATES)


class TestShipmentPurchase(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()
        carrier = models.Carrier.objects.get(carrier_id="canadapost")
        self.shipment.rates = [
            {
                "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
                "carrier_id": "canadapost",
                "carrier_name": "canadapost",
                "currency": "CAD",
                "extra_charges": [
                    {"amount": 101.83, "currency": "CAD", "name": "Base charge"},
                    {"amount": 2.7, "currency": "CAD", "name": "Fuel surcharge"},
                    {"amount": -11.74, "currency": "CAD", "name": "SMB Savings"},
                    {"amount": -9.04, "currency": "CAD", "name": "Discount"},
                    {"amount": 13.92, "currency": "CAD", "name": "Duties and taxes"},
                ],
                "service": "canadapost_priority",
                "total_charge": 106.71,
                "transit_days": 2,
                "test_mode": True,
                "meta": {
                    "rate_provider": "canadapost",
                    "service_name": "CANADAPOST PRIORITY",
                    "carrier_connection_id": carrier.pk,
                },
            }
        ]
        self.shipment.save()

    def test_purchase_shipment(self):
        url = reverse(
            "karrio.server.manager:shipment-purchase",
            kwargs=dict(pk=self.shipment.pk),
        )
        data = SHIPMENT_PURCHASE_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PURCHASED_SHIPMENT)

        # Assert a tracker is created for the newly purchased shipment
        self.assertTrue(
            models.Tracking.objects.filter(
                tracking_number=PURCHASED_SHIPMENT["tracking_number"]
            ).exists()
        )

    def test_cancel_shipment(self):
        url = reverse(
            "karrio.server.manager:shipment-details",
            kwargs=dict(pk=self.shipment.pk),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            response = self.client.delete(url)
            response_data = json.loads(response.content)

            mock.assert_not_called()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_RESPONSE)

    def test_cancel_purchased_shipment(self):
        url = reverse(
            "karrio.server.manager:shipment-details",
            kwargs=dict(pk=self.shipment.pk),
        )
        self.shipment.status = "purchased"
        self.shipment.shipment_identifier = "123456789012"
        self.shipment.selected_rate_carrier = self.carrier
        self.shipment.save()

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_CANCEL_VALUE
            response = self.client.delete(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_PURCHASED_RESPONSE)

        self.assertFalse(
            models.Tracking.objects.filter(
                tracking_number=self.shipment.tracking_number,
            ).exists()
        )


SHIPMENT_DATA = {
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
}

SHIPMENT_RATES = {
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
                {"name": "Duty and taxes", "amount": 13.92, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                {"name": "Base surcharge", "amount": 101.83, "currency": "CAD"},
            ],
            "meta": {
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        }
    ]
}

SHIPMENT_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "status": "draft",
    "carrier_name": None,
    "carrier_id": None,
    "label_type": "PDF",
    "label_url": None,
    "invoice_url": None,
    "meta": {},
    "metadata": {},
    "tracking_number": None,
    "shipment_identifier": None,
    "selected_rate": None,
    "selected_rate_id": None,
    **SHIPMENT_RATES,
    "tracking_url": None,
    "tracker_id": None,
    "shipper": {
        "id": ANY,
        "object_type": "address",
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
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
    },
    "recipient": {
        "id": ANY,
        "object_type": "address",
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
            "width": 42.0,
            "height": 32.0,
            "length": 32.0,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "items": [],
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "freight_class": None,
            "reference_number": ANY,
            "options": {},
        }
    ],
    "payment": {"account_number": None, "currency": "CAD", "paid_by": "sender"},
    "services": [],
    "options": {"shipment_date": ANY},
    "customs": None,
    "reference": None,
    "carrier_ids": ["canadapost"],
    "service": None,
    "created_at": ANY,
    "test_mode": True,
    "messages": [],
}

SHIPMENT_OPTIONS = {
    "options": {"insurance": 54, "currency": "CAD", "shipment_date": "2020-01-01"},
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

SHIPMENT_PURCHASE_DATA = {"selected_rate_id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4"}

SELECTED_RATE = {
    "id": ANY,
    "object_type": "rate",
    "carrier_id": "canadapost",
    "carrier_name": "canadapost",
    "currency": "CAD",
    "extra_charges": [
        {"amount": 2.7, "currency": "CAD", "name": "Fuel surcharge"},
        {"amount": -11.74, "currency": "CAD", "name": "SMB Savings"},
    ],
    "service": "canadapost_priority",
    "total_charge": 106.71,
    "transit_days": 2,
    "meta": {
        "carrier_connection_id": ANY,
        "rate_provider": "canadapost",
        "service_name": "CANADAPOST PRIORITY",
    },
    "test_mode": True,
}

CREATED_SHIPMENT_RESPONSE = (
    ShipmentDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        tracking_number="123456789012",
        shipment_identifier="123456789012",
        docs=dict(label="==apodifjoefr"),
    ),
    [],
)

RETURNED_CANCEL_VALUE = (
    ConfirmationDetails(
        carrier_name="canadapost",
        carrier_id="canadapost",
        success=True,
        operation="Cancel Shipment",
    ),
    [],
)

PURCHASED_SHIPMENT = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": "/v1/trackers/canadapost/123456789012",
    "shipper": {
        "id": ANY,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
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
    "recipient": {
        "id": ANY,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "514 000 9999",
        "state_code": "BC",
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
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
            "reference_number": "123456789012",
            "object_type": "parcel",
            "options": {},
        }
    ],
    "services": [],
    "options": {"shipment_date": ANY},
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
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD"},
            ],
            "meta": {
                "service_name": "CANADAPOST PRIORITY",
                "rate_provider": "canadapost",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        }
    ],
    "reference": None,
    "label_type": "PDF",
    "carrier_ids": [],
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
            {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
            {"name": "Discount", "amount": -9.04, "currency": "CAD"},
            {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD"},
        ],
        "meta": {
            "service_name": "CANADAPOST PRIORITY",
            "rate_provider": "canadapost",
            "carrier_connection_id": ANY,
        },
        "test_mode": True,
    },
    "meta": {"rate_provider": "canadapost", "service_name": "CANADAPOST PRIORITY"},
    "service": "canadapost_priority",
    "selected_rate_id": ANY,
    "test_mode": True,
    "label_url": ANY,
    "invoice_url": None,
}

CANCEL_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": None,
    "shipper": {
        "id": ANY,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
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
    "recipient": {
        "id": ANY,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "514 000 9999",
        "state_code": "BC",
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
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
            "object_type": "parcel",
            "options": {},
        }
    ],
    "services": [],
    "options": {},
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
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD"},
            ],
            "meta": {
                "carrier_connection_id": ANY,
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        }
    ],
    "reference": None,
    "label_type": None,
    "carrier_ids": [],
    "tracker_id": None,
    "created_at": ANY,
    "metadata": {},
    "messages": [],
    "status": "cancelled",
    "carrier_name": None,
    "carrier_id": None,
    "tracking_number": None,
    "shipment_identifier": None,
    "selected_rate": None,
    "meta": {},
    "service": None,
    "selected_rate_id": None,
    "test_mode": True,
    "label_url": None,
    "invoice_url": None,
}

CANCEL_PURCHASED_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": None,
    "shipper": {
        "id": ANY,
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "John Poop",
        "company_name": "A corp.",
        "country_code": "CA",
        "email": None,
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
    "recipient": {
        "id": ANY,
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "federal_tax_id": None,
        "state_tax_id": None,
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "email": None,
        "phone_number": "514 000 9999",
        "state_code": "BC",
        "suburb": None,
        "residential": False,
        "address_line1": "5840 Oak St",
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
            "object_type": "parcel",
            "options": {},
        }
    ],
    "services": [],
    "options": {},
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
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD"},
            ],
            "meta": {
                "carrier_connection_id": ANY,
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        }
    ],
    "reference": None,
    "label_type": None,
    "carrier_ids": [],
    "tracker_id": None,
    "created_at": ANY,
    "metadata": {},
    "messages": [],
    "status": "cancelled",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "tracking_number": None,
    "shipment_identifier": "123456789012",
    "selected_rate": None,
    "meta": {},
    "service": None,
    "selected_rate_id": None,
    "test_mode": True,
    "label_url": None,
    "invoice_url": None,
}
