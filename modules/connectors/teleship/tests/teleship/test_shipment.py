"""Teleship carrier shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/shipments/labels",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)

        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/shipments/labels/SHP-UK-US-98765/void",
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "123 Business Park",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "state_code": "LDN",
        "person_name": "John Smith",
        "company_name": "UK Exports Ltd",
        "phone_number": "+442071234567",
        "email": "shipping@ukexports.co.uk",
    },
    "recipient": {
        "address_line1": "555 Industrial Blvd",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Jane Doe",
        "company_name": "US Imports Inc",
        "phone_number": "+13105551234",
        "email": "receiving@usimports.com",
    },
    "parcels": [
        {
            "weight": 1.2,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "packaging_type": "parcel",
        }
    ],
    "service": "teleship_expedited_dropoff",
    "reference": "UK-US-12345",
    "label_type": "PDF",
    "customs": {
        "content_type": "merchandise",
        "invoice": "INV-2025-001",
        "invoice_date": "2025-01-15",
        "commodities": [
            {
                "sku": "WIDGET-001",
                "title": "Electronic Widget",
                "description": "Consumer electronics widget",
                "quantity": 2,
                "weight": 0.6,
                "weight_unit": "KG",
                "value_amount": 150.00,
                "value_currency": "GBP",
                "origin_country": "GB",
            }
        ],
        "options": {"eori_number": "GB123456789000"},
    },
}

ShipmentCancelPayload = {"shipment_identifier": "SHP-UK-US-98765"}

ShipmentRequest = [
    {
        "commercialInvoiceReference": "INV-2025-001",
        "commodities": [
            {
                "countryOfOrigin": "GB",
                "description": "Consumer electronics widget",
                "quantity": 2,
                "sku": "WIDGET-001",
                "title": "Electronic Widget",
                "unitWeight": {"unit": "kg", "value": 0.6},
                "value": {"amount": 150.0, "currency": "GBP"},
            }
        ],
        "customerReference": "UK-US-12345",
        "customs": {
            "EORI": "GB123456789000",
            "contentType": "CommercialGoods",
            "invoiceDate": "2025-01-15",
            "invoiceNumber": "INV-2025-001",
        },
        "dimensions": {"height": 15.0, "length": 30.0, "unit": "cm", "width": 20.0},
        "packageType": "parcel",
        "serviceCode": "TELESHIP-EXPEDITED-DROPOFF",
        "shipFrom": {
            "address": {
                "city": "London",
                "country": "GB",
                "line1": "123 Business Park",
                "postcode": "SW1A 1AA",
                "state": "LDN",
            },
            "company": "UK Exports Ltd",
            "email": "shipping@ukexports.co.uk",
            "name": "John Smith",
            "phone": "+442071234567",
        },
        "shipTo": {
            "address": {
                "city": "Los Angeles",
                "country": "US",
                "line1": "555 Industrial Blvd",
                "postcode": "90001",
                "state": "CA",
            },
            "company": "US Imports Inc",
            "email": "receiving@usimports.com",
            "name": "Jane Doe",
            "phone": "+13105551234",
        },
        "weight": {"unit": "kg", "value": 1.2},
    }
]

ShipmentCancelRequest = {"shipmentId": "SHP-UK-US-98765"}

ShipmentResponse = """{
    "shipment": {
        "shipmentId": "SHP-UK-US-98765",
        "trackingNumber": "TELESHIP12345678901",
        "status": "label_created",
        "customerReference": "UK-US-12345",
        "shipDate": "2025-01-15T00:00:00.00Z",
        "estimatedDelivery": "2025-01-20T00:00:00.00Z",
        "packageType": "parcel",
        "documents": [
            {
                "type": "LABEL",
                "format": "PDF",
                "url": "https://labels.teleship.com/SHP-UK-US-98765.pdf",
                "base64String": "JVBERi0xLjcKJeLjz9MK..."
            }
        ],
        "weight": {
            "value": 1.2,
            "unit": "kg"
        },
        "dimensions": {
            "length": 30,
            "width": 20,
            "height": 15,
            "unit": "cm"
        },
        "shipTo": {
            "name": "Jane Doe",
            "email": "receiving@usimports.com",
            "phone": "+13105551234",
            "address": {
                "line1": "555 Industrial Blvd",
                "city": "Los Angeles",
                "state": "CA",
                "postcode": "90001",
                "country": "US"
            }
        },
        "shipFrom": {
            "name": "John Smith",
            "company": "UK Exports Ltd",
            "address": {
                "line1": "123 Business Park",
                "city": "London",
                "state": "LDN",
                "postcode": "SW1A 1AA",
                "country": "GB"
            }
        },
        "rate": {
            "price": 106.56,
            "currency": "GBP",
            "transit": 3,
            "estimatedDelivery": "2025-01-20T00:00:00.00Z",
            "service": {
                "name": "Teleship Expedited Drop-off",
                "code": "TELESHIP-EXPEDITED-DROPOFF"
            },
            "charges": [
                {
                    "name": "Base Freight",
                    "amount": 85.00,
                    "currency": "GBP"
                },
                {
                    "name": "Fuel Surcharge",
                    "amount": 12.75,
                    "currency": "GBP"
                },
                {
                    "name": "Customs Clearance",
                    "amount": 8.81,
                    "currency": "GBP"
                }
            ]
        }
    }
}"""

ErrorResponse = """{
    "messages": [
        {
            "code": 422,
            "timestamp": "2025-01-15T10:30:45Z",
            "message": "Shipment creation failed",
            "details": [
                "Invalid customs declaration for international shipment",
                "EORI number format is invalid",
                "Commodity value must be specified for customs clearance"
            ]
        }
    ]
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "tracking_number": "TELESHIP12345678901",
        "shipment_identifier": "SHP-UK-US-98765",
        "label_type": "PDF",
        "docs": {"label": "JVBERi0xLjcKJeLjz9MK..."},
        "meta": {
            "customer_reference": "UK-US-12345",
            "service_name": "teleship_expedited_dropoff",
            "ship_date": "2025-01-15T00:00:00.00Z",
        },
        "selected_rate": {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "service": "teleship_expedited_dropoff",
            "total_charge": 106.56,
            "currency": "GBP",
            "transit_days": 3,
            "estimated_delivery": "2025-01-20",
            "extra_charges": [
                {"name": "Base Freight", "amount": 85.0, "currency": "GBP"},
                {"name": "Fuel Surcharge", "amount": 12.75, "currency": "GBP"},
                {"name": "Customs Clearance", "amount": 8.81, "currency": "GBP"},
            ],
            "meta": {"service_name": "teleship_expedited_dropoff"},
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "422",
            "message": "Shipment creation failed",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Invalid customs declaration for international shipment",
                    "EORI number format is invalid",
                    "Commodity value must be specified for customs clearance",
                ],
            },
        }
    ],
]
