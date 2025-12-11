"""DPD Group carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class TestDPDGroupShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_shipment_cancel_request(self.ShipmentCancelRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/SHIP123456/cancel"
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 10.0,
        "height": 10.0,
        "length": 10.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }],
    "service": "express"
}

ShipmentCancelPayload = {
    "shipment_identifier": "SHIP123456"
}

ShipmentRequest = {
    "shipper": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weightUnit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimensionUnit": "CM",
            "packagingType": "BOX"
        }
    ],
    "serviceCode": "express",
    "labelFormat": "PDF"
}

ShipmentCancelRequest = {
    "shipmentIdentifier": "SHIP123456"
}

ShipmentResponse = """{
  "shipment": {
    "trackingNumber": "1Z999999999999999",
    "shipmentId": "SHIP123456",
    "labelData": {
      "format": "PDF",
      "image": "base64_encoded_label_data"
    },
    "invoiceImage": "base64_encoded_invoice_data",
    "serviceCode": "express"
  }
}"""

ShipmentCancelResponse = """{
  "success": true,
  "message": "Shipment successfully cancelled"
}"""

ErrorResponse = """{
  "error": {
    "code": "shipment_error",
    "message": "Unable to create shipment",
    "details": "Invalid shipment information provided"
  }
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "dpd_group",
        "carrier_name": "dpd_group",
        "tracking_number": "1Z999999999999999",
        "shipment_identifier": "SHIP123456",
        "label_type": "PDF",
        "docs": {
            "label": "base64_encoded_label_data",
            "invoice": "base64_encoded_invoice_data"
        },
        "meta": {
            "service_code": "express"
        }
    },
    []
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "dpd_group",
        "carrier_name": "dpd_group",
        "success": True,
        "operation": "Cancel Shipment"
    },
    []
]

ParsedErrorResponse = [
    {},
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "code": "shipment_error",
            "message": "Unable to create shipment",
            "details": {
                "details": "Invalid shipment information provided"
            }
        }
    ]
]