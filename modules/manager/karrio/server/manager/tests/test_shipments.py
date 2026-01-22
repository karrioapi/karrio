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
from karrio.server.core.utils import create_carrier_snapshot
import karrio.server.manager.models as models
import karrio.server.providers.models as providers


class TestShipmentFixture(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        # Shipper and recipient as dict data for JSON fields (use proper JSON-generated ID format)
        self.shipper_data = {
            "id": "adr_111122223333",
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
            "street_number": None,
            "residential": False,
            "address_line1": "125 Church St",
            "address_line2": None,
            "validate_location": False,
            "validation": None,
        }
        self.recipient_data = {
            "id": "adr_444455556666",
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
            "street_number": None,
            "residential": False,
            "address_line1": "5840 Oak St",
            "address_line2": None,
            "validate_location": False,
            "validation": None,
        }
        self.parcel_data = {
            "id": "pcl_777788889999",
            "weight": 1.0,
            "weight_unit": "KG",
            "width": None,
            "height": None,
            "length": None,
            "dimension_unit": None,
            "packaging_type": None,
            "package_preset": "canadapost_corrugated_small_box",
            "description": None,
            "content": None,
            "is_document": False,
            "freight_class": None,
            "reference_number": None,
            "items": [],
            "options": {},
            "meta": {},
        }
        self.shipment: models.Shipment = models.Shipment.objects.create(
            shipper=self.shipper_data,
            recipient=self.recipient_data,
            parcels=[self.parcel_data],
            created_by=self.user,
            test_mode=True,
            payment={"currency": "CAD", "paid_by": "sender"},
        )


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
        carrier = providers.CarrierConnection.objects.get(carrier_id="canadapost")
        self.shipment.rates = [
            {
                "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
                "carrier_id": "canadapost",
                "carrier_name": "canadapost",
                "currency": "CAD",
                "estimated_delivery": None,
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
            "karrio.server.manager:shipment-cancel",
            kwargs=dict(pk=self.shipment.pk),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            response = self.client.post(url)
            response_data = json.loads(response.content)

            mock.assert_not_called()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_RESPONSE)

    def test_cancel_purchased_shipment(self):
        url = reverse(
            "karrio.server.manager:shipment-cancel",
            kwargs=dict(pk=self.shipment.pk),
        )
        self.shipment.status = "purchased"
        self.shipment.shipment_identifier = "123456789012"
        # Set selected_rate and carrier snapshot
        self.shipment.selected_rate = {
            **self.shipment.rates[0],
        }
        self.shipment.carrier = create_carrier_snapshot(self.carrier)
        self.shipment.save()

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_CANCEL_VALUE
            response = self.client.post(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, CANCEL_PURCHASED_RESPONSE)

        self.assertFalse(
            models.Tracking.objects.filter(
                tracking_number=self.shipment.tracking_number,
            ).exists()
        )

    def test_purchase_shipment_with_has_alternative_services(self):
        """
        Test that when has_alternative_services is enabled and service is requested
        but not in rates, the purchase proceeds by delegating service resolution to the carrier.
        """
        url = reverse(
            "karrio.server.manager:shipment-purchase",
            kwargs=dict(pk=self.shipment.pk),
        )
        self.shipment.options = {"has_alternative_services": True}
        self.shipment.save()
        data = {"service": "canadapost_expedited_parcel"}

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)  # type: ignore
        self.assertDictEqual(
            dict(status=response_data["status"], service=response_data["service"]),
            dict(status="purchased", service="canadapost_expedited_parcel"),
        )


class TestSingleCallLabelPurchase(APITestCase):
    """Test single call label purchase via POST to shipment-list with a service specified."""

    def test_single_call_label_purchase(self):
        """
        Test that when a shipment is created with a service specified,
        the label is purchased in a single call after fetching rates.
        """
        url = reverse("karrio.server.manager:shipment-list")
        data = SINGLE_CALL_LABEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [RETURNED_RATES_VALUE, CREATED_SHIPMENT_RESPONSE]
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)  # type: ignore
        self.assertDictEqual(
            {
                "status": response_data["status"],
                "carrier_name": response_data["carrier_name"],
                "service": response_data["service"],
                "tracking_number": response_data["tracking_number"],
                "services": response_data["services"],
                "rates_count": len(response_data["rates"]),
            },
            {
                "status": "purchased",
                "carrier_name": "canadapost",
                "service": "canadapost_priority",
                "tracking_number": "123456789012",
                "services": ["canadapost_priority"],
                "rates_count": 1,
            },
        )


class TestSingleCallWithAlternativeServices(APITestCase):
    """Test single call label purchase with has_alternative_services flag (skip rate fetching)."""

    def test_single_call_label_purchase_skip_rates(self):
        """
        Test that when has_alternative_services=True and service is specified,
        rate fetching is skipped and label is purchased directly.
        Carrier is resolved from the service name.
        """
        url = reverse("karrio.server.manager:shipment-list")
        data = SINGLE_CALL_SKIP_RATES_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            # Verify only 1 call was made (rates were skipped)
            self.assertEqual(mock.call_count, 1)

        self.assertResponseNoErrors(response)  # type: ignore
        self.assertDictEqual(
            {
                "status": response_data["status"],
                "carrier_name": response_data["carrier_name"],
                "service": response_data["service"],
                "tracking_number": response_data["tracking_number"],
                "has_alternative_services": response_data["selected_rate"]["meta"].get(
                    "has_alternative_services"
                ),
            },
            {
                "status": "purchased",
                "carrier_name": "canadapost",
                "service": "canadapost_priority",
                "tracking_number": "123456789012",
                "has_alternative_services": True,
            },
        )

    def test_single_call_label_purchase_skip_rates_with_carrier_ids(self):
        """
        Test that when has_alternative_services=True, service, and carrier_ids are specified,
        rate fetching is skipped and label is purchased directly.
        """
        url = reverse("karrio.server.manager:shipment-list")
        data = {**SINGLE_CALL_SKIP_RATES_DATA, "carrier_ids": ["canadapost"]}

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            # Verify only 1 call was made (rates were skipped)
            self.assertEqual(mock.call_count, 1)

        self.assertResponseNoErrors(response)  # type: ignore
        self.assertDictEqual(
            {
                "status": response_data["status"],
                "carrier_name": response_data["carrier_name"],
                "service": response_data["service"],
                "tracking_number": response_data["tracking_number"],
                "has_alternative_services": response_data["selected_rate"]["meta"].get(
                    "has_alternative_services"
                ),
            },
            {
                "status": "purchased",
                "carrier_name": "canadapost",
                "service": "canadapost_priority",
                "tracking_number": "123456789012",
                "has_alternative_services": True,
            },
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
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {
                    "name": "Duty and taxes",
                    "amount": 13.92,
                    "currency": "CAD",
                    "id": ANY,
                },
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": ANY},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": ANY},
                {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": ANY},
                {
                    "name": "Base surcharge",
                    "amount": 101.83,
                    "currency": "CAD",
                    "id": ANY,
                },
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
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
        "street_number": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "validation": None,
        "meta": {},
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
            "meta": {},
        }
    ],
    "payment": {"account_number": None, "currency": "CAD", "paid_by": "sender"},
    "return_address": None,
    "billing_address": None,
    "services": [],
    "options": {"shipping_date": ANY, "shipment_date": ANY},
    "customs": None,
    "reference": None,
    "carrier_ids": ["canadapost"],
    "service": None,
    "created_at": ANY,
    "test_mode": True,
    "messages": [],
    "shipping_documents": [],
}

SHIPMENT_OPTIONS = {
    "options": {
        "insurance": 54,
        "currency": "CAD",
        "shipment_date": "2050-01-01",
        "shipping_date": "2050-01-01T10:30",
    },
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
    "estimated_delivery": None,
    "extra_charges": [
        {"amount": 2.7, "currency": "CAD", "name": "Fuel surcharge"},
        {"amount": -11.74, "currency": "CAD", "name": "SMB Savings"},
    ],
    "service": "canadapost_priority",
    "total_charge": 106.71,
    "transit_days": 2,
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
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
        "id": "adr_111122223333",
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
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "recipient": {
        "id": "adr_444455556666",
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
        "street_number": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "parcels": [
        {
            "id": "pcl_777788889999",
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
            "reference_number": ANY,
            "object_type": "parcel",
            "options": {},
            "meta": {},
        }
    ],
    "services": [],
    "options": {"shipping_date": ANY, "shipment_date": ANY},
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "return_address": None,
    "billing_address": None,
    "customs": None,
    "rates": [
        {
            "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": None,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": None},
                {
                    "name": "Duties and taxes",
                    "amount": 13.92,
                    "currency": "CAD",
                    "id": None,
                },
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
        "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
        "object_type": "rate",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "currency": "CAD",
        "estimated_delivery": None,
        "service": "canadapost_priority",
        "total_charge": 106.71,
        "transit_days": 2,
        "extra_charges": [
            {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": None},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": None},
            {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": None},
            {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD", "id": None},
        ],
        "meta": {
            "ext": "canadapost",
            "carrier": "canadapost",
            "service_name": "CANADAPOST PRIORITY",
            "rate_provider": "canadapost",
            "carrier_connection_id": ANY,
        },
        "test_mode": True,
    },
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "rate_provider": "canadapost",
        "service_name": "CANADAPOST PRIORITY",
    },
    "service": "canadapost_priority",
    "selected_rate_id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
    "test_mode": True,
    "label_url": ANY,
    "invoice_url": None,
    "shipping_documents": [
        {
            "category": "label",
            "format": "PDF",
            "url": ANY,
            "base64": "==apodifjoefr",
        }
    ],
}

CANCEL_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": None,
    "shipper": {
        "id": "adr_111122223333",
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
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "recipient": {
        "id": "adr_444455556666",
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
        "street_number": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "parcels": [
        {
            "id": "pcl_777788889999",
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
            "reference_number": ANY,
            "object_type": "parcel",
            "options": {},
            "meta": {},
        }
    ],
    "services": [],
    "options": {},
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "return_address": None,
    "billing_address": None,
    "customs": None,
    "rates": [
        {
            "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": None,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {
                    "name": "Base charge",
                    "amount": 101.83,
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
                    "name": "Duties and taxes",
                    "amount": 13.92,
                    "currency": "CAD",
                    "id": None,
                },
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
    "shipping_documents": [],
}

CANCEL_PURCHASED_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "tracking_url": None,
    "shipper": {
        "id": "adr_111122223333",
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
        "street_number": None,
        "residential": False,
        "address_line1": "125 Church St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "recipient": {
        "id": "adr_444455556666",
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
        "street_number": None,
        "residential": False,
        "address_line1": "5840 Oak St",
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
        "meta": {},
    },
    "parcels": [
        {
            "id": "pcl_777788889999",
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
            "reference_number": ANY,
            "object_type": "parcel",
            "options": {},
            "meta": {},
        }
    ],
    "services": [],
    "options": {},
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "return_address": None,
    "billing_address": None,
    "customs": None,
    "rates": [
        {
            "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": None,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {
                    "name": "Base charge",
                    "amount": 101.83,
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
                    "name": "Duties and taxes",
                    "amount": 13.92,
                    "currency": "CAD",
                    "id": None,
                },
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
    "selected_rate": {
        "id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
        "object_type": "rate",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "currency": "CAD",
        "estimated_delivery": None,
        "service": "canadapost_priority",
        "total_charge": 106.71,
        "transit_days": 2,
        "extra_charges": [
            {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": None},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": None},
            {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": None},
            {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD", "id": None},
        ],
        "meta": {
            "carrier_connection_id": ANY,
            "rate_provider": "canadapost",
            "service_name": "CANADAPOST PRIORITY",
        },
        "test_mode": True,
    },
    "meta": {},
    "service": "canadapost_priority",
    "selected_rate_id": "rat_f5c1317021cb4b3c8a5d3b7369ed99e4",
    "test_mode": True,
    "label_url": None,
    "invoice_url": None,
    "shipping_documents": [],
}

SINGLE_CALL_LABEL_DATA = {
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
    "service": "canadapost_priority",
    "carrier_ids": ["canadapost"],
    "options": {"insurance": 100},
}

SINGLE_CALL_SKIP_RATES_DATA = {
    # Note: No carrier_ids provided - carrier is resolved from service name
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
    "service": "canadapost_priority",
    "options": {"has_alternative_services": True},
}


class TestShipmentDocumentDownload(APITestCase):
    """Test shipment document download POST API."""

    def create_purchased_shipment(self):
        """Create and purchase a shipment via API."""
        url = reverse("karrio.server.manager:shipment-list")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.side_effect = [RETURNED_RATES_VALUE, CREATED_SHIPMENT_RESPONSE]
            response = self.client.post(url, SINGLE_CALL_LABEL_DATA)
            return json.loads(response.content)

    def test_download_label_document(self):
        shipment = self.create_purchased_shipment()

        url = reverse(
            "karrio.server.manager:shipment-document-download",
            kwargs=dict(pk=shipment["id"], doc="label"),
        )
        response = self.client.post(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response_data,
            LABEL_DOCUMENT_RESPONSE,
        )

    def test_download_document_not_found(self):
        # Create a draft shipment (no label)
        url = reverse("karrio.server.manager:shipment-list")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, SHIPMENT_DATA)
            shipment = json.loads(response.content)

        url = reverse(
            "karrio.server.manager:shipment-document-download",
            kwargs=dict(pk=shipment["id"], doc="label"),
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_download_invalid_document_type(self):
        shipment = self.create_purchased_shipment()

        url = reverse(
            "karrio.server.manager:shipment-document-download",
            kwargs=dict(pk=shipment["id"], doc="invalid"),
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_download_shipment_not_found(self):
        url = reverse(
            "karrio.server.manager:shipment-document-download",
            kwargs=dict(pk="shp_non_existent_id", doc="label"),
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestShipmentCancelIdempotent(APITestCase):
    """Test shipment cancel idempotency."""

    def test_cancel_already_cancelled_shipment_returns_202(self):
        # Create a shipment via API
        url = reverse("karrio.server.manager:shipment-list")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, SHIPMENT_DATA)
            shipment = json.loads(response.content)

        # Cancel the shipment first time
        cancel_url = reverse(
            "karrio.server.manager:shipment-cancel",
            kwargs=dict(pk=shipment["id"]),
        )
        self.client.post(cancel_url)

        # Cancel again - should return 202
        response = self.client.post(cancel_url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response_data["status"], "cancelled")


class TestComputeEstimatedDelivery(APITestCase):
    """Test compute_estimated_delivery utility function."""

    def test_returns_estimated_delivery_from_rate(self):
        """Test that estimated_delivery is returned directly from selected_rate."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {"estimated_delivery": "2024-01-20", "transit_days": 5}
        options = {"shipping_date": "2024-01-15"}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertEqual(estimated_delivery, "2024-01-20")
        self.assertEqual(shipping_date_str, "2024-01-15")

    def test_computes_from_transit_days_when_no_estimated_delivery(self):
        """Test that estimated_delivery is computed from transit_days when not provided."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {"transit_days": 5}
        options = {"shipping_date": "2024-01-15"}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertEqual(estimated_delivery, "2024-01-20")
        self.assertEqual(shipping_date_str, "2024-01-15")

    def test_uses_shipment_date_option_as_fallback(self):
        """Test that shipment_date is used when shipping_date is not available."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {"transit_days": 3}
        options = {"shipment_date": "2024-01-10"}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertEqual(estimated_delivery, "2024-01-13")
        self.assertEqual(shipping_date_str, "2024-01-10")

    def test_returns_none_when_no_transit_days_or_estimated_delivery(self):
        """Test that None is returned when neither estimated_delivery nor transit_days are available."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {}
        options = {"shipping_date": "2024-01-15"}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertIsNone(estimated_delivery)
        self.assertEqual(shipping_date_str, "2024-01-15")

    def test_returns_none_when_no_shipping_date(self):
        """Test that None is returned when no shipping date is available."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {"transit_days": 5}
        options = {}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertIsNone(estimated_delivery)
        self.assertIsNone(shipping_date_str)

    def test_handles_none_inputs(self):
        """Test that None inputs are handled gracefully."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        estimated_delivery, shipping_date_str = compute_estimated_delivery(None, None)

        self.assertIsNone(estimated_delivery)
        self.assertIsNone(shipping_date_str)

    def test_handles_datetime_format_shipping_date(self):
        """Test that datetime format shipping_date is handled correctly."""
        from karrio.server.manager.serializers import compute_estimated_delivery

        selected_rate = {"transit_days": 2}
        options = {"shipping_date": "2024-01-15T10:30"}

        estimated_delivery, shipping_date_str = compute_estimated_delivery(
            selected_rate, options
        )

        self.assertEqual(estimated_delivery, "2024-01-17")
        self.assertEqual(shipping_date_str, "2024-01-15T10:30")


LABEL_DOCUMENT_RESPONSE = {
    "category": "label",
    "format": "PDF",
    "print_format": None,
    "base64": "==apodifjoefr",
    "url": ANY,
}
