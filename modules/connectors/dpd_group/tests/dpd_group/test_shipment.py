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

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
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
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# Test Data

ShipmentPayload = {
    "shipper": {
        "company_name": "Acme Corporation",
        "address_line1": "Main Street 123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
        "person_name": "John Shipper",
        "phone_number": "+49301234567",
        "email": "shipper@example.com",
    },
    "recipient": {
        "company_name": "Doe Enterprises",
        "address_line1": "Oak Avenue 456",
        "city": "Munich",
        "postal_code": "54321",
        "country_code": "DE",
        "person_name": "Jane Recipient",
        "phone_number": "+49891234567",
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "length": 30,
            "width": 20,
            "height": 15,
            "description": "Electronics",
        }
    ],
    "service": "dpd_group_classic",
    "reference": "ORDER-12345",
    "label_type": "PDF",
}

ShipmentRequest = {
    "shipperAddress": {
        "name": "John Shipper",
        "company": "Acme Corporation",
        "street": "Main Street",
        "houseNumber": "123",
        "postalCode": "12345",
        "city": "Berlin",
        "country": "DE",
        "email": "shipper@example.com",
        "phone": "+49301234567",
    },
    "receiverAddress": {
        "name": "Jane Recipient",
        "company": "Doe Enterprises",
        "street": "Oak Avenue",
        "houseNumber": "456",
        "postalCode": "54321",
        "city": "Munich",
        "country": "DE",
        "email": "receiver@example.com",
        "phone": "+49891234567",
    },
    "parcels": [
        {
            "weight": 5.0,
            "length": 30,
            "width": 20,
            "height": 15,
            "content": "Electronics",
            "customerReferenceNumber1": "ORDER-12345",
        }
    ],
    "productCode": "CL",
    "orderNumber": "ORDER-12345",
    "labelFormat": "PDF",
}

ShipmentResponse = """{
  "shipmentId": "SHIP123456789",
  "shipmentNumber": "05300000011267",
  "parcels": [
    {
      "parcelNumber": "05300000011267",
      "trackingNumber": "05300000011267",
      "parcelId": "PARCEL-001"
    }
  ],
  "label": {
    "format": "PDF",
    "content": "JVBERi0xLjQKJeLjz9MKM...",
    "encoding": "BASE64"
  },
  "shipmentDate": "2024-01-15",
  "trackingUrl": "https://tracking.dpdgroup.com/track/05300000011267",
  "services": {
    "productCode": "CL",
    "productName": "DPD Classic"
  }
}"""

ErrorResponse = """{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "recipient.postalCode",
        "message": "Postal code is required"
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "path": "/api/v1.1/shipments",
  "status": 400
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "dpd_group",
        "carrier_name": "dpd_group",
        "tracking_number": "05300000011267",
        "shipment_identifier": "SHIP123456789",
        "label_type": "PDF",
        "docs": {
            "label": "JVBERi0xLjQKJeLjz9MKM..."
        },
        "meta": {
            "shipment_number": "05300000011267",
            "tracking_url": "https://tracking.dpdgroup.com/track/05300000011267",
            "service_name": "DPD Classic",
        },
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "code": "VALIDATION_ERROR",
            "message": "Invalid request parameters",
            "details": {
                "details": [
                    {
                        "field": "recipient.postalCode",
                        "message": "Postal code is required"
                    }
                ]
            }
        }
    ]
]
