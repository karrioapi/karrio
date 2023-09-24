import unittest
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
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
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

ParsedShipmentResponse = [{}, []]

ParsedCancelShipmentResponse = [{}, []]


ShipmentRequest = {
    "accountNumber": "account_number",
    "subAccountNumber": "sub_account_number",
    "processingLocation": "SFO",
    "includeRate": True,
    "labelType": "PDF",
    "orderNumber": "string",
    "dispatchNumber": "string",
    "packageID": "string",
    "recipientTaxID": "string",
    "returnFirstName": "string",
    "returnLastName": "string",
    "returnCompanyName": "string",
    "returnAddressLine1": "string",
    "returnAddressLine2": "string",
    "returnAddressLine3": "string",
    "returnCity": "string",
    "returnProvince": "string",
    "returnPostalCode": "string",
    "returnCountryCode": "string",
    "returnPhone": "string",
    "returnEmail": "user@example.com",
    "recipientFirstName": "string",
    "recipientLastName": "string",
    "recipientBusinessName": "string",
    "recipientAddressLine1": "string",
    "recipientAddressLine2": "string",
    "recipientAddressLine3": "string",
    "recipientCity": "string",
    "recipientProvince": "string",
    "recipientPostalCode": "string",
    "recipientCountryCode": "string",
    "recipientPhone": "string",
    "recipientEmail": "user@example.com",
    "totalPackageWeight": 0,
    "weightUnit": "Lb",
    "dimLength": 0,
    "dimWidth": 0,
    "dimHeight": 0,
    "dimUnit": "IN",
    "totalPackageValue": 0,
    "currencyType": "USD",
    "productCode": "string",
    "customerReferenceNumber1": "string",
    "customerReferenceNumber2": "string",
    "customerReferenceNumber3": "string",
    "contentType": "M",
    "packageContentDescription": "string",
    "vatNumber": "string",
    "sellerName": "string",
    "sellerAddressLine1": "string",
    "sellerAddressLine2": "string",
    "sellerAddressLine3": "string",
    "sellerCity": "string",
    "sellerProvince": "string",
    "sellerPostalCode": "string",
    "sellerCountryCode": "string",
    "sellerPhone": "string",
    "sellerEmail": "user@example.com",
    "items": [
        {
            "sku": "string",
            "itemDescription": "string",
            "unitPrice": 0,
            "quantity": 0,
            "unitWeight": 0,
            "countryOfOrigin": "string",
            "htsNumber": "string",
        }
    ],
}


ShipmentCancelRequest = {
    "accountNumber": "string",
    "subAccountNumber": "string",
    "packageID": "string",
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
  "responseStatusCode": 0,
  "responseStatusMessage": "string"
}
"""
