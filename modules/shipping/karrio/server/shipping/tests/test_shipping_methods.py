import json
from unittest.mock import ANY, patch
from django.urls import reverse
from rest_framework import status
from karrio.core.models import (
    RateDetails,
    ChargeDetails,
    ShipmentDetails,
)
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.shipping.models as models
import karrio.server.manager.models as manager_models
import karrio.server.providers.models as providers


class TestShippingMethodFixture(GraphTestCase):
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
                    "carrier_service": "canadapost_regular_parcel",
                    "carrier_ids": ["canadapost"],
                    "carrier_options": {"insurance": 100},
                    "metadata": {"key": "value"},
                    "is_active": True,
                }
            },
        )

        self.shipping_method = models.ShippingMethod.objects.get(
            id=response.data["data"]["create_shipping_method"]["shipping_method"]["id"]
        )

        # Create shipment via API (without service to keep it in draft status)
        url = reverse("karrio.server.manager:shipment-list")
        shipment_data = {
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

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            shipment_response = self.client.post(url, shipment_data)
            shipment_response_data = json.loads(shipment_response.content)

        self.shipment = manager_models.Shipment.objects.get(
            id=shipment_response_data["id"]
        )


class TestShippingMethodList(GraphTestCase):
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
                    "carrier_ids": ["canadapost"],
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
                    "carrier_ids": ["ups_package"],
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


class TestBuyShippingMethodLabel(TestShippingMethodFixture):
    def test_buy_method_label(self):
        url = reverse(
            "karrio.server.shipping:buy-method-label",
            kwargs=dict(pk=self.shipping_method.pk),
        )
        data = LABEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, LABEL_RESPONSE)


class TestBuyShipmentLabel(TestShippingMethodFixture):
    def setUp(self) -> None:
        super().setUp()

        # Fetch rates via API (keeps shipment in draft but adds rates)
        rates_url = reverse(
            "karrio.server.manager:shipment-rates", kwargs=dict(pk=self.shipment.pk)
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_RATES_VALUE
            rates_response = self.client.post(rates_url, {})
            rates_response_data = json.loads(rates_response.content)

        # Refresh shipment to get the rates
        self.shipment.refresh_from_db()

    def test_buy_shipment_label(self):
        url = reverse(
            "karrio.server.shipping:buy-shipment-label",
            kwargs=dict(pk=self.shipping_method.pk, shipment_id=self.shipment.pk),
        )
        data = SHIPMENT_LABEL_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = CREATED_SHIPMENT_RESPONSE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PURCHASED_SHIPMENT_RESPONSE)

        # Assert a tracker is created for the newly purchased shipment
        self.assertTrue(
            manager_models.Tracking.objects.filter(
                tracking_number=PURCHASED_SHIPMENT_RESPONSE["tracking_number"]
            ).exists()
        )


SHIPPING_METHOD_RESPONSE_1 = {
    "id": ANY,
    "object_type": "shipping-method",
    "name": "Standard Shipping",
    "slug": "standard-shipping",
    "description": "Regular delivery",
    "carrier_code": "ups",
    "carrier_service": "ups_ground",
    "carrier_ids": ["ups_package"],
    "carrier_options": {},
    "metadata": {},
    "is_active": True,
    "test_mode": True,
    "created_at": ANY,
}

SHIPPING_METHOD_RESPONSE_2 = {
    "id": ANY,
    "object_type": "shipping-method",
    "name": "Express Shipping",
    "slug": "express-shipping",
    "description": "Fast delivery",
    "carrier_code": "canadapost",
    "carrier_service": "canadapost_priority",
    "carrier_ids": ["canadapost"],
    "carrier_options": {},
    "metadata": {},
    "is_active": True,
    "test_mode": True,
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
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=5,
            service="canadapost_regular_parcel",
            total_charge=95.71,
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

LABEL_RESPONSE = {
    "id": ANY,
    "object_type": "shipment",
    "status": "purchased",
    "carrier_name": "canadapost",
    "carrier_id": "canadapost",
    "label_type": "PDF",
    "label_url": ANY,
    "invoice_url": None,
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "rate_provider": "canadapost",
        "service_name": "CANADAPOST REGULAR PARCEL",
    },
    "metadata": {},
    "tracking_number": "123456789012",
    "shipment_identifier": "123456789012",
    "selected_rate": {
        "id": ANY,
        "object_type": "rate",
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "currency": "CAD",
        "estimated_delivery": ANY,
        "service": "canadapost_regular_parcel",
        "total_charge": 95.71,
        "transit_days": 5,
        "extra_charges": [
            {"name": "Duty and taxes", "amount": 13.92, "currency": "CAD", "id": ANY},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": ANY},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": ANY},
            {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": ANY},
            {"name": "Base surcharge", "amount": 101.83, "currency": "CAD", "id": ANY},
        ],
        "meta": {
            "ext": "canadapost",
            "carrier": "canadapost",
            "service_name": "CANADAPOST REGULAR PARCEL",
            "rate_provider": "canadapost",
            "carrier_connection_id": ANY,
        },
        "test_mode": True,
    },
    "selected_rate_id": ANY,
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_regular_parcel",
            "total_charge": 95.71,
            "transit_days": 5,
            "extra_charges": [
                {"name": "Duty and taxes", "amount": 13.92, "currency": "CAD", "id": ANY},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": ANY},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": ANY},
                {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": ANY},
                {"name": "Base surcharge", "amount": 101.83, "currency": "CAD", "id": ANY},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST REGULAR PARCEL",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        }
    ],
    "tracking_url": "/v1/trackers/canadapost/123456789012",
    "tracker_id": ANY,
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
    "return_address": None,
    "billing_address": None,
    "services": [],
    "options": {"shipping_date": ANY, "shipment_date": ANY, "insurance": 100},
    "customs": None,
    "reference": None,
    "carrier_ids": ["canadapost"],
    "service": "canadapost_regular_parcel",
    "created_at": ANY,
    "test_mode": True,
    "messages": [],
}

SHIPMENT_LABEL_DATA = {
    "label_type": "PDF",
    "options": {
        "currency": "CAD",
    },
    "metadata": {},
}

PURCHASED_SHIPMENT_RESPONSE = {
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
        "street_number": None,
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
        "street_number": None,
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
            "reference_number": ANY,
            "object_type": "parcel",
            "options": {},
        }
    ],
    "services": [],
    "options": {"shipping_date": ANY, "shipment_date": ANY, "insurance": 100},
    "payment": {"paid_by": "sender", "currency": "CAD", "account_number": None},
    "return_address": None,
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
            "service": "canadapost_regular_parcel",
            "total_charge": 95.71,
            "transit_days": 5,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": ANY},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": ANY},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": ANY},
                {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": ANY},
                {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD", "id": ANY},
            ],
            "meta": {
                "service_name": "CANADAPOST REGULAR PARCEL",
                "rate_provider": "canadapost",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
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
        "estimated_delivery": ANY,
        "service": "canadapost_regular_parcel",
        "total_charge": 95.71,
        "transit_days": 5,
        "extra_charges": [
            {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": ANY},
            {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD", "id": ANY},
            {"name": "SMB Savings", "amount": -11.74, "currency": "CAD", "id": ANY},
            {"name": "Discount", "amount": -9.04, "currency": "CAD", "id": ANY},
            {"name": "Duties and taxes", "amount": 13.92, "currency": "CAD", "id": ANY},
        ],
        "meta": {
            "ext": "canadapost",
            "carrier": "canadapost",
            "service_name": "CANADAPOST REGULAR PARCEL",
            "rate_provider": "canadapost",
            "carrier_connection_id": ANY,
        },
        "test_mode": True,
    },
    "meta": {
        "ext": "canadapost",
        "carrier": "canadapost",
        "rate_provider": "canadapost",
        "service_name": "CANADAPOST REGULAR PARCEL",
    },
    "service": "canadapost_regular_parcel",
    "selected_rate_id": ANY,
    "test_mode": True,
    "label_url": ANY,
    "invoice_url": None,
}
