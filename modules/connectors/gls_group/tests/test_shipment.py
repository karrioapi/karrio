"""GLS Group carrier shipment tests."""

import unittest
from unittest.mock import patch
from tests.fixture import gateway, shipper_address, recipient_address
import logging
import karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestGLSGroupShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        # Basic validation
        request_dict = lib.to_dict(request.serialize())
        self.assertIn("shipment", request_dict)
        self.assertIn("sender", request_dict["shipment"])
        self.assertIn("receiver", request_dict["shipment"])
        self.assertIn("parcels", request_dict["shipment"])

    def test_create_shipment(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rs/shipments"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertIsNotNone(parsed_response[0])
            self.assertIsInstance(parsed_response[0], models.ShipmentDetails)

    def test_parse_error_response(self):
        with patch("karrio.mappers.gls_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertIsNone(parsed_response[0])
            self.assertTrue(len(parsed_response[1]) > 0)


if __name__ == "__main__":
    unittest.main()

# Test data
ShipmentPayload = {
    "shipper": {
        "company_name": "Test Shipper Company",
        "address_line1": "Main Street",
        "address_line2": "123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
        "person_name": "John Doe",
        "phone_number": "+49301234567",
        "email": "shipper@example.com",
    },
    "recipient": {
        "company_name": "Test Recipient Company",
        "address_line1": "Market Street",
        "address_line2": "456",
        "city": "Munich",
        "postal_code": "54321",
        "country_code": "DE",
        "person_name": "Jane Smith",
        "phone_number": "+49891234567",
        "email": "recipient@example.com",
    },
    "parcels": [
        {
            "weight": 5.5,
            "length": 30,
            "width": 20,
            "height": 15,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "service": "gls_parcel",
    "reference": "TEST123",
}

ShipmentResponse = """{
  "shipmentId": "GLS123456789",
  "trackingNumbers": ["12345678901234567890"],
  "parcels": [
    {
      "parcelId": "P001",
      "trackingNumber": "12345678901234567890",
      "weight": 5.5
    }
  ],
  "labels": [
    {
      "trackingNumber": "12345678901234567890",
      "labelData": "JVBERi0xLjQKJeLjz9MK",
      "labelFormat": "PDF"
    }
  ],
  "createdAt": "2025-01-15T10:30:00Z",
  "shippingDate": "2025-01-16",
  "status": "CREATED"
}"""

ErrorResponse = """{
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid request parameters",
      "field": "shipment.recipient.postalCode"
    }
  ]
}"""
