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

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize())["shipment"], ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
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
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
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
    }],
    "service": "mydhl_express_worldwide"
}

ShipmentRequest = {
    "plannedShippingDateAndTime": ANY,
    "pickup": {"isRequested": False},
    "productCode": "P",
    "localProductCode": "P",
    "getRateEstimates": True,
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "outputImageProperties": {
        "printerDPI": 300,
        "encodingFormat": "pdf",
        "imageOptions": [
            {"typeCode": "label", "templateName": "ECOM26_84_001", "isRequested": True}
        ]
    },
    "customerDetails": {
        "shipperDetails": {
            "postalAddress": {
                "postalCode": "90001",
                "cityName": "Los Angeles",
                "countryCode": "US",
                "provinceCode": "CA",
                "addressLine1": "123 Main Street",
                "countryName": "United States"
            },
            "contactInformation": {
                "email": "shipper@example.com",
                "phone": "1234567890",
                "mobilePhone": "1234567890",
                "companyName": "Test Company",
                "fullName": "John Doe"
            },
            "typeCode": "business"
        },
        "receiverDetails": {
            "postalAddress": {
                "postalCode": "10001",
                "cityName": "New York",
                "countryCode": "US",
                "provinceCode": "NY",
                "addressLine1": "456 Broadway",
                "countryName": "United States"
            },
            "contactInformation": {
                "email": "recipient@example.com",
                "phone": "0987654321",
                "mobilePhone": "0987654321",
                "companyName": "Recipient Corp",
                "fullName": "Jane Smith"
            },
            "typeCode": "business"
        }
    },
    "content": {
        "packages": [
            {
                "typeCode": "YP",
                "weight": 5.0,
                "dimensions": {"length": 25, "width": 20, "height": 15}
            }
        ],
        "isCustomsDeclarable": False,
        "description": "Shipment",
        "unitOfMeasurement": "metric"
    }
}

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
