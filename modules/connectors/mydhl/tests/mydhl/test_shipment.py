"""MyDHL carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestMyDHLShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        print(f"Generated cancel request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            print(f"Called cancel method")
            # MyDHL doesn't support shipment cancellation via API, so no URL call is made

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )
            print(f"Cancel response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "123 Main Street",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "John Doe",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "shipper@example.com"
    },
    "recipient": {
        "address_line1": "456 Broadway",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
        "person_name": "Jane Smith",
        "company_name": "Recipient Corp",
        "phone_number": "0987654321",
        "email": "recipient@example.com"
    },
    "parcels": [{
        "weight": 5.0,
        "width": 20.0,
        "height": 15.0,
        "length": 25.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }],
    "service": "express_worldwide"
}

ShipmentCancelPayload = {
    "shipment_identifier": "9356579890"
}

ShipmentRequest = {
    "shipper": {
        "addressLine1": "123 Main Street",
        "city": "Los Angeles",
        "postalCode": "90001",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "John Doe",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "shipper@example.com"
    },
    "recipient": {
        "addressLine1": "456 Broadway",
        "city": "New York",
        "postalCode": "10001",
        "countryCode": "US",
        "stateCode": "NY",
        "personName": "Jane Smith",
        "companyName": "Recipient Corp",
        "phoneNumber": "0987654321",
        "email": "recipient@example.com"
    },
    "packages": [
        {
            "weight": 5.0,
            "weightUnit": "kg",
            "length": 25.0,
            "width": 20.0,
            "height": 15.0,
            "dimensionUnit": "cm",
            "packagingType": ANY
        }
    ],
    "serviceCode": ANY,
    "customerNumber": "123456789",
    "labelFormat": "PDF"
}

ShipmentCancelRequest = "9356579890"

ShipmentResponse = """{
  "shipmentTrackingNumber": 9356579890,
  "trackingUrl": "https://www.dhl.com/tracking?trackingNumber=9356579890",
  "packages": [
    {
      "referenceNumber": 1,
      "trackingNumber": "9356579890",
      "trackingUrl": "https://www.dhl.com/tracking?trackingNumber=9356579890"
    }
  ],
  "documents": [
    {
      "imageFormat": "PDF",
      "content": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAwIFI+PgplbmRvYmoKMiAwIG9iago8PC9UeXBlL1BhZ2VzL0tpZHNbMyAwIFJdL0NvdW50IDE+PgplbmRvYmoKMyAwIG9iago8PC9UeXBlL1BhZ2UvTWVkaWFCb3hbMCAwIDYxMiA3OTJdL1BhcmVudCAyIDAgUi9SZXNvdXJjZXM8PC9Gb250PDw+Pj4+Pj4KZW5kb2JqCnRyYWlsZXIKPDwvUm9vdCAxIDAgUj4+Cg=="
    }
  ]
}"""

ShipmentCancelResponse = """{
  "status": 400,
  "title": "Not Supported",
  "detail": "MyDHL does not support shipment cancellation via API. Please contact DHL customer service to cancel a shipment.",
  "instance": "/shipments"
}"""

ErrorResponse = """{
  "status": 400,
  "title": "Bad Request",
  "detail": "Invalid shipment request - missing required field",
  "instance": "/shipments"
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "tracking_number": "9356579890",
        "shipment_identifier": "9356579890",
        "label_type": "PDF",
        "docs": {
            "label": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAwIFI+PgplbmRvYmoKMiAwIG9iago8PC9UeXBlL1BhZ2VzL0tpZHNbMyAwIFJdL0NvdW50IDE+PgplbmRvYmoKMyAwIG9iago8PC9UeXBlL1BhZ2UvTWVkaWFCb3hbMCAwIDYxMiA3OTJdL1BhcmVudCAyIDAgUi9SZXNvdXJjZXM8PC9Gb250PDw+Pj4+Pj4KZW5kb2JqCnRyYWlsZXIKPDwvUm9vdCAxIDAgUj4+Cg=="
        },
        "meta": {
            "tracking_url": "https://www.dhl.com/tracking?trackingNumber=9356579890",
            "package_tracking_numbers": ["9356579890"]
        }
    },
    []
]

ParsedShipmentCancelResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "MyDHL does not support shipment cancellation via API. Please contact DHL customer service to cancel a shipment.",
            "details": {
                "instance": "/shipments",
                "title": "Not Supported"
            }
        }
    ]
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "400",
            "message": "Invalid shipment request - missing required field",
            "details": {
                "instance": "/shipments",
                "title": "Bad Request"
            }
        }
    ]
]