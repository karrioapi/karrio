import unittest
import urllib.parse
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAsendiaUSShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package?{urllib.parse.urlencode(lib.to_dict(ShipmentCancelRequest))}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "1234567890",
        "state_code": "OK",
    },
    "recipient": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [
        {
            "width": 5.0,
            "height": 5.0,
            "length": 3.0,
            "weight": 1.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "service": "asendia_us_fully_tracked",
}


ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "asendia_us",
        "carrier_name": "asendia_us",
        "docs": {"label": "string"},
        "label_type": "string",
        "meta": {"package_id": "string"},
        "shipment_identifier": "string",
        "tracking_number": "string",
    },
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "code": "Continue",
            "details": {},
            "message": "string",
        }
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "asendia_us",
        "carrier_name": "asendia_us",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [
        {
            "carrier_id": "asendia_us",
            "carrier_name": "asendia_us",
            "code": 200,
            "details": {},
            "message": "string",
        }
    ],
]


ShipmentRequest = {
    "accountNumber": "account_number",
    "includeRate": True,
    "processingLocation": "SFO",
    "productCode": "65",
    "recipientAddressLine1": "1098 N Fraser Street",
    "recipientBusinessName": "ABC Corp.",
    "recipientCity": "Georgetown",
    "recipientCountryCode": "US",
    "recipientFirstName": "Tall Tom",
    "recipientLastName": "Tall Tom",
    "recipientPhone": "8005554526",
    "recipientPostalCode": "29440",
    "recipientProvince": "SC",
    "returnAddressLine1": "1309 S Agnew Avenue",
    "returnAddressLine2": "Apt 303",
    "returnCity": "Oklahoma City",
    "returnCompanyName": "Horizon",
    "returnCountryCode": "US",
    "returnFirstName": "Lina Smith",
    "returnLastName": "Lina Smith",
    "returnPhone": "1234567890",
    "returnPostalCode": "73108",
    "returnProvince": "OK",
    "sellerAddressLine1": "1309 S Agnew Avenue",
    "sellerAddressLine2": "Apt 303",
    "sellerCity": "Oklahoma City",
    "sellerCountryCode": "US",
    "sellerName": "Horizon",
    "sellerPhone": "1234567890",
    "sellerPostalCode": "73108",
    "sellerProvince": "OK",
    "totalPackageWeight": 1.0,
    "weightUnit": "Lb",
}


ShipmentCancelRequest = {
    "accountNumber": "account_number",
    "packageID": "794947717776",
}


ShipmentResponse = """{
  "shippingRates": [
    {
      "productCode": "string",
      "rate": 0,
      "currencyType": "string"
    }
  ],
  "packageLabel": {
    "packageId": "string",
    "trackingNumber": "string",
    "labels": [
      {
        "name": "string",
        "type": "string",
        "content": "string"
      }
    ]
  },
  "responseStatus": {
    "responseStatusCode": "Continue",
    "responseStatusMessage": "string"
  }
}
"""

ShipmentCancelResponse = """{
  "responseStatusCode": 200,
  "responseStatusMessage": "string"
}
"""
