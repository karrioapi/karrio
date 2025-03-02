import json
from typing import Tuple
from unittest.mock import ANY, patch
from django.http.response import HttpResponse
from django.urls import reverse
from rest_framework import status
from karrio.core.models import (
    RateDetails,
    ChargeDetails,
)
from karrio.server.core.tests import APITestCase
import karrio.server.manager.models as manager
import karrio.server.orders.models as models


class TestOrderFixture(APITestCase):
    def create_order(self) -> Tuple[HttpResponse, dict]:
        url = reverse("karrio.server.orders:order-list")
        data = ORDER_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        return response, response_data


class TestOrders(TestOrderFixture):
    def test_create_order(self):
        response, response_data = self.create_order()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, ORDER_RESPONSE)

    def test_duplicate_order_creation(self):
        # Create the first order successfully
        response1, _ = self.create_order()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Attempt to create another order with the same order_id/source pair
        response2, _ = self.create_order()

        # The second request should fail with a conflict error
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)


class TestOrderDetails(TestOrderFixture):
    def test_retrieve_order(self):
        _, data = self.create_order()
        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=data["id"]))
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, ORDER_RESPONSE)

    def test_cancel_order(self):
        _, order = self.create_order()
        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=order["id"]))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.Order.objects.get(pk=order["id"]).status == "cancelled")

    def test_cannot_cancel_fulfilled_order(self):
        _, data = self.create_order()
        order = models.Order.objects.get(pk=data["id"])
        order.status = "fulfilled"
        order.save()

        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=data["id"]))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_cannot_cancel_delivered_order(self):
        _, data = self.create_order()
        order = models.Order.objects.get(pk=data["id"])
        order.status = "delivered"
        order.save()

        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=data["id"]))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class TestOrderShipments(TestOrderFixture):
    # def test_linked_shipment(self):
    #     _, order = self.create_order()

    #     # Create shipment
    #     with patch("karrio.server.core.gateway.utils.identity") as mock:
    #         shipment_url = reverse("karrio.server.manager:shipment-list")
    #         data = SHIPMENT_DATA
    #         data["parcels"][0]["items"][0]["parent_id"] = order["line_items"][0]["id"]
    #         mock.return_value = RETURNED_RATES_VALUE
    #         shipment_response = self.client.post(shipment_url, data)
    #         shipment_data = json.loads(shipment_response.content)

    #         self.assertEqual(shipment_response.status_code, status.HTTP_201_CREATED)

    #     # Fetch related order
    #     url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=order["id"]))
    #     response = self.client.get(url)
    #     response_data = json.loads(response.content)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertDictEqual(response_data, ORDER_SHIPMENTS_RESPONSE)

    def test_partial_order_when_some_items_are_fulfilled(self):
        _, order = self.create_order()

        # Create shipment and change status to purchased
        with patch("karrio.server.core.gateway.utils.identity") as mock:
            shipment_url = reverse("karrio.server.manager:shipment-list")
            data = {
                **SHIPMENT_DATA,
                "parcels": [
                    {
                        **SHIPMENT_DATA["parcels"][0],
                        "items": [
                            {
                                **SHIPMENT_DATA["parcels"][0]["items"][0],
                                "parent_id": order["line_items"][0]["id"],
                            }
                        ],
                    }
                ],
            }
            mock.return_value = RETURNED_RATES_VALUE
            shipment_response = self.client.post(shipment_url, data)
            shipment_data = json.loads(shipment_response.content)
            shipment = manager.Shipment.objects.get(pk=shipment_data["id"])
            shipment.status = "purchased"
            shipment.save()

        # Fetch related order
        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=order["id"]))
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, PARTIAL_ORDER_RESPONSE)

    def test_fulfilled_order_when_all_items_are_fulfilled(self):
        _, order = self.create_order()

        # Create shipment and change status to purchased
        with patch("karrio.server.core.gateway.utils.identity") as mock:
            shipment_url = reverse("karrio.server.manager:shipment-list")
            data = {
                **SHIPMENT_DATA,
                "parcels": [
                    {
                        **SHIPMENT_DATA["parcels"][0],
                        "items": [
                            {
                                **SHIPMENT_DATA["parcels"][0]["items"][0],
                                "parent_id": order["line_items"][0]["id"],
                            },
                            {
                                "parent_id": order["line_items"][1]["id"],
                                "weight": 1.7,
                                "weight_unit": "KG",
                                "description": None,
                                "title": "Red Leather Coat",
                                "quantity": 1,
                                "sku": None,
                                "hs_code": None,
                                "value_amount": 129.99,
                                "value_currency": "USD",
                                "metadata": {"id": 1071823172},
                            },
                        ],
                    }
                ],
            }
            mock.return_value = RETURNED_RATES_VALUE
            shipment_response = self.client.post(shipment_url, data)
            shipment_data = json.loads(shipment_response.content)

            self.assertEqual(shipment_response.status_code, status.HTTP_201_CREATED)
            shipment = manager.Shipment.objects.get(pk=shipment_data["id"])
            shipment.status = "purchased"
            shipment.save()

        # Fetch related order
        url = reverse("karrio.server.orders:order-detail", kwargs=dict(pk=order["id"]))
        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, FULFILLED_ORDER_RESPONSE)


ORDER_DATA = {
    "order_id": "1073459962",
    "source": "shopify",
    "shipping_to": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "country_code": "CA",
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "address_line1": "125 Church St",
    },
    "line_items": [
        {
            "weight": 1.7,
            "weight_unit": "KG",
            "title": "Red Leather Coat",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 129.99,
            "value_currency": "USD",
            "metadata": {"id": 1071823172},
        },
        {
            "weight": 0.75,
            "weight_unit": "KG",
            "title": "Blue Suede Shoes",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 85.95,
            "value_currency": "USD",
            "metadata": {"id": 1071823173},
        },
    ],
}

ORDER_RESPONSE = {
    "id": ANY,
    "object_type": "order",
    "order_id": "1073459962",
    "order_date": ANY,
    "source": "shopify",
    "status": "unfulfilled",
    "shipping_to": {
        "id": ANY,
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
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "shipping_from": None,
    "billing_address": None,
    "line_items": [
        {
            "id": ANY,
            "weight": 1.7,
            "weight_unit": "KG",
            "description": None,
            "title": "Red Leather Coat",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 129.99,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823172},
            "object_type": "commodity",
            "unfulfilled_quantity": 1,
        },
        {
            "id": ANY,
            "weight": 0.75,
            "weight_unit": "KG",
            "description": None,
            "title": "Blue Suede Shoes",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 85.95,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823173},
            "object_type": "commodity",
            "unfulfilled_quantity": 1,
        },
    ],
    "options": {},
    "meta": {},
    "metadata": {},
    "shipments": [],
    "test_mode": True,
    "created_at": ANY,
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
                ChargeDetails(amount=101.83, currency="CAD", name="Base charge"),
                ChargeDetails(amount=-9.04, currency="CAD", name="Discount"),
                ChargeDetails(amount=2.7, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-11.74, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=13.92, currency="CAD", name="Duties and taxes"),
            ],
        )
    ],
    [],
]

SHIPMENT_DATA = {
    "shipper": {
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "person_name": "Jane Doe",
        "company_name": "B corp.",
        "country_code": "CA",
        "phone_number": "+1 514-000-0000",
        "state_code": "BC",
        "residential": True,
        "address_line1": "5840 Oak St",
    },
    "recipient": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "person_name": "John Doe",
        "company_name": "A corp.",
        "country_code": "CA",
        "phone_number": "+1 514-000-0000",
        "state_code": "NB",
        "address_line1": "125 Church St",
    },
    "parcels": [
        {
            "weight": 2,
            "width": 46,
            "height": 38,
            "length": 32,
            "package_preset": "canadapost_corrugated_medium_box",
            "is_document": False,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "freight_class": None,
            "reference_number": None,
            "items": [
                {
                    "weight": 0.75,
                    "weight_unit": "KG",
                    "title": "Blue Suede Shoes",
                    "quantity": 1,
                    "value_amount": 85.95,
                    "value_currency": "USD",
                    "metadata": {"id": 1071823173},
                }
            ],
            "options": {},
        }
    ],
    "options": {"currency": "CAD"},
    "carrier_ids": ["canadapost"],
}

ORDER_SHIPMENTS_RESPONSE = {
    "id": ANY,
    "object_type": "order",
    "order_id": "1073459962",
    "order_date": ANY,
    "source": "shopify",
    "status": "unfulfilled",
    "shipping_to": {
        "id": ANY,
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
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "shipping_from": None,
    "billing_address": None,
    "line_items": [
        {
            "id": ANY,
            "weight": 1.7,
            "weight_unit": "KG",
            "description": None,
            "title": "Red Leather Coat",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 129.99,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823172},
            "object_type": "commodity",
            "unfulfilled_quantity": 1,
        },
        {
            "id": ANY,
            "weight": 0.75,
            "weight_unit": "KG",
            "description": None,
            "title": "Blue Suede Shoes",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 85.95,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823173},
            "object_type": "commodity",
            "unfulfilled_quantity": 1,
        },
    ],
    "options": {},
    "meta": {},
    "metadata": {},
    "shipments": [
        {
            "id": ANY,
            "object_type": "shipment",
            "tracking_url": None,
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
                "phone_number": "+1 514-000-0000",
                "state_code": "BC",
                "street_number": None,
                "residential": True,
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
                "person_name": "John Doe",
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
                "object_type": "address",
                "validation": None,
            },
            "parcels": [
                {
                    "id": ANY,
                    "weight": 2.0,
                    "width": 46.0,
                    "height": 38.0,
                    "length": 32.0,
                    "packaging_type": None,
                    "package_preset": "canadapost_corrugated_medium_box",
                    "description": None,
                    "content": None,
                    "is_document": False,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "items": [
                        {
                            "id": ANY,
                            "weight": 0.75,
                            "weight_unit": "KG",
                            "description": None,
                            "title": "Blue Suede Shoes",
                            "quantity": 1,
                            "sku": None,
                            "hs_code": None,
                            "value_amount": 85.95,
                            "value_currency": "USD",
                            "origin_country": None,
                            "parent_id": ANY,
                            "metadata": {"id": 1071823173},
                            "object_type": "commodity",
                        }
                    ],
                    "reference_number": ANY,
                    "freight_class": None,
                    "options": {},
                    "object_type": "parcel",
                }
            ],
            "services": [],
            "options": {"currency": "CAD", "shipment_date": ANY, "shipping_date": ANY},
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
                    "transit_days": 2,
                    "extra_charges": [
                        {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                        {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                        {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                        {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                        {
                            "name": "Duties and taxes",
                            "amount": 13.92,
                            "currency": "CAD",
                        },
                    ],
                    "meta": {
                        "ext": "canadapost",
                        "carrier": "canadapost",
                        "service_name": "CANADAPOST PRIORITY",
                        "rate_provider": "canadapost",
                        "carrier_connection_id": ANY,
                    },
                    "test_mode": True,
                }
            ],
            "reference": None,
            "label_type": "PDF",
            "carrier_ids": ["canadapost"],
            "tracker_id": None,
            "created_at": ANY,
            "metadata": {},
            "messages": [],
            "status": "draft",
            "carrier_name": None,
            "carrier_id": None,
            "tracking_number": None,
            "shipment_identifier": None,
            "selected_rate": None,
            "meta": {"orders": ANY},
            "service": None,
            "selected_rate_id": None,
            "test_mode": True,
            "label_url": None,
            "invoice_url": None,
        }
    ],
    "test_mode": True,
    "created_at": ANY,
}

FULFILLED_ORDER_RESPONSE = {
    "id": ANY,
    "object_type": "order",
    "order_id": "1073459962",
    "order_date": ANY,
    "source": "shopify",
    "status": "fulfilled",
    "shipping_to": {
        "id": ANY,
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
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "shipping_from": None,
    "billing_address": None,
    "line_items": [
        {
            "id": ANY,
            "weight": 1.7,
            "weight_unit": "KG",
            "description": None,
            "title": "Red Leather Coat",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 129.99,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823172},
            "object_type": "commodity",
            "unfulfilled_quantity": 0,
        },
        {
            "id": ANY,
            "weight": 0.75,
            "weight_unit": "KG",
            "description": None,
            "title": "Blue Suede Shoes",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 85.95,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823173},
            "object_type": "commodity",
            "unfulfilled_quantity": 0,
        },
    ],
    "options": {},
    "meta": {},
    "metadata": {},
    "shipments": [
        {
            "id": ANY,
            "object_type": "shipment",
            "tracking_url": None,
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
                "phone_number": "+1 514-000-0000",
                "state_code": "BC",
                "street_number": None,
                "residential": True,
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
                "person_name": "John Doe",
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
                "object_type": "address",
                "validation": None,
            },
            "parcels": [
                {
                    "id": ANY,
                    "weight": 2.0,
                    "width": 46.0,
                    "height": 38.0,
                    "length": 32.0,
                    "packaging_type": None,
                    "package_preset": "canadapost_corrugated_medium_box",
                    "description": None,
                    "content": None,
                    "is_document": False,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "items": [
                        {
                            "id": ANY,
                            "weight": 0.75,
                            "weight_unit": "KG",
                            "description": None,
                            "title": "Blue Suede Shoes",
                            "quantity": 1,
                            "sku": None,
                            "hs_code": None,
                            "value_amount": 85.95,
                            "value_currency": "USD",
                            "origin_country": None,
                            "parent_id": ANY,
                            "metadata": {"id": 1071823173},
                            "object_type": "commodity",
                        },
                        {
                            "id": ANY,
                            "weight": 1.7,
                            "weight_unit": "KG",
                            "description": None,
                            "title": "Red Leather Coat",
                            "quantity": 1,
                            "sku": None,
                            "hs_code": None,
                            "value_amount": 129.99,
                            "value_currency": "USD",
                            "origin_country": None,
                            "parent_id": ANY,
                            "metadata": {"id": 1071823172},
                            "object_type": "commodity",
                        },
                    ],
                    "freight_class": None,
                    "reference_number": ANY,
                    "object_type": "parcel",
                    "options": {},
                }
            ],
            "services": [],
            "options": {"currency": "CAD", "shipment_date": ANY, "shipping_date": ANY},
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
                    "transit_days": 2,
                    "extra_charges": [
                        {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                        {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                        {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                        {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                        {
                            "name": "Duties and taxes",
                            "amount": 13.92,
                            "currency": "CAD",
                        },
                    ],
                    "meta": {
                        "ext": "canadapost",
                        "carrier": "canadapost",
                        "service_name": "CANADAPOST PRIORITY",
                        "rate_provider": "canadapost",
                        "carrier_connection_id": ANY,
                    },
                    "test_mode": True,
                }
            ],
            "reference": None,
            "return_address": None,
            "label_type": "PDF",
            "carrier_ids": ["canadapost"],
            "tracker_id": None,
            "created_at": ANY,
            "metadata": {},
            "messages": [],
            "status": "purchased",
            "carrier_name": None,
            "carrier_id": None,
            "tracking_number": None,
            "shipment_identifier": None,
            "selected_rate": None,
            "meta": {"orders": ANY},
            "service": None,
            "selected_rate_id": None,
            "test_mode": True,
            "label_url": None,
            "invoice_url": None,
        }
    ],
    "test_mode": True,
    "created_at": ANY,
}

PARTIAL_ORDER_RESPONSE = {
    "id": ANY,
    "object_type": "order",
    "order_id": "1073459962",
    "order_date": ANY,
    "source": "shopify",
    "status": "partial",
    "shipping_to": {
        "id": ANY,
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
        "address_line2": None,
        "validate_location": False,
        "object_type": "address",
        "validation": None,
    },
    "shipping_from": None,
    "billing_address": None,
    "line_items": [
        {
            "id": ANY,
            "weight": 1.7,
            "weight_unit": "KG",
            "description": None,
            "title": "Red Leather Coat",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 129.99,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823172},
            "object_type": "commodity",
            "unfulfilled_quantity": 0,
        },
        {
            "id": ANY,
            "weight": 0.75,
            "weight_unit": "KG",
            "description": None,
            "title": "Blue Suede Shoes",
            "quantity": 1,
            "sku": None,
            "hs_code": None,
            "value_amount": 85.95,
            "value_currency": "USD",
            "origin_country": None,
            "parent_id": None,
            "metadata": {"id": 1071823173},
            "object_type": "commodity",
            "unfulfilled_quantity": 1,
        },
    ],
    "meta": {},
    "options": {},
    "metadata": {},
    "shipments": [
        {
            "id": ANY,
            "object_type": "shipment",
            "tracking_url": None,
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
                "phone_number": "+1 514-000-0000",
                "state_code": "BC",
                "street_number": None,
                "residential": True,
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
                "person_name": "John Doe",
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
                "object_type": "address",
                "validation": None,
            },
            "parcels": [
                {
                    "id": ANY,
                    "weight": 2.0,
                    "width": 46.0,
                    "height": 38.0,
                    "length": 32.0,
                    "packaging_type": None,
                    "package_preset": "canadapost_corrugated_medium_box",
                    "description": None,
                    "content": None,
                    "is_document": False,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "items": [
                        {
                            "id": ANY,
                            "weight": 0.75,
                            "weight_unit": "KG",
                            "description": None,
                            "title": "Blue Suede Shoes",
                            "quantity": 1,
                            "sku": None,
                            "hs_code": None,
                            "value_amount": 85.95,
                            "value_currency": "USD",
                            "origin_country": None,
                            "parent_id": ANY,
                            "metadata": {"id": 1071823173},
                            "object_type": "commodity",
                        }
                    ],
                    "reference_number": ANY,
                    "freight_class": None,
                    "options": {},
                    "object_type": "parcel",
                }
            ],
            "services": [],
            "options": {"currency": "CAD", "shipment_date": ANY, "shipping_date": ANY},
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
                    "transit_days": 2,
                    "extra_charges": [
                        {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                        {"name": "Discount", "amount": -9.04, "currency": "CAD"},
                        {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                        {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                        {
                            "name": "Duties and taxes",
                            "amount": 13.92,
                            "currency": "CAD",
                        },
                    ],
                    "meta": {
                        "ext": "canadapost",
                        "carrier": "canadapost",
                        "service_name": "CANADAPOST PRIORITY",
                        "rate_provider": "canadapost",
                        "carrier_connection_id": ANY,
                    },
                    "test_mode": True,
                }
            ],
            "reference": None,
            "return_address": None,
            "label_type": "PDF",
            "carrier_ids": ["canadapost"],
            "tracker_id": None,
            "created_at": ANY,
            "metadata": {},
            "messages": [],
            "status": "purchased",
            "carrier_name": None,
            "carrier_id": None,
            "tracking_number": None,
            "shipment_identifier": None,
            "selected_rate": None,
            "meta": {"orders": ANY},
            "service": None,
            "selected_rate_id": None,
            "test_mode": True,
            "label_url": None,
            "invoice_url": None,
        }
    ],
    "test_mode": True,
    "created_at": ANY,
}
