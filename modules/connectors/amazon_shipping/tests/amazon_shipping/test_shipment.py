"""Amazon Shipping shipment tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestAmazonShippingShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**SHIPMENT_PAYLOAD)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**CANCEL_SHIPMENT_PAYLOAD)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertDictEqual(request.serialize(), ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)

        self.assertEqual(request.serialize(), CancelShipmentRequestJSON)

    def test_create_shipment(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v2/oneClickShipment",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v2/shipments/{self.ShipmentCancelRequest.shipment_identifier}/cancel",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            with patch("karrio.providers.amazon_shipping.shipment.create.lib.image_to_pdf") as pdf_mock:
                pdf_mock.return_value = "base64_pdf_label"
                parsed_response = response.parse()

                self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            parsed_response = karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedCancelShipmentResponse)


if __name__ == "__main__":
    unittest.main()


SHIPMENT_PAYLOAD = {
    "service": "amazon_shipping_standard",
    "reference": "order #1111",
    "recipient": {
        "company_name": "AmazonShipping",
        "address_line1": "417 Montgomery Street",
        "address_line2": "5th Floor",
        "city": "San Francisco",
        "state_code": "CA",
        "postal_code": "94104",
        "country_code": "US",
        "phone_number": "415-528-7555",
        "email": "recipient@example.com",
    },
    "shipper": {
        "person_name": "George Costanza",
        "company_name": "Vandelay Industries",
        "address_line1": "1 E 161st St.",
        "city": "Bronx",
        "state_code": "NY",
        "postal_code": "10451",
        "country_code": "US",
        "email": "shipper@example.com",
    },
    "parcels": [{"length": 9.0, "width": 6.0, "height": 2.0, "weight": 10.0}],
}

CANCEL_SHIPMENT_PAYLOAD = {
    "shipment_identifier": "shipment-12345",
}

ShipmentRequestJSON = {
    "shipFrom": {
        "name": "Vandelay Industries",
        "addressLine1": "1 E 161st St.",
        "companyName": "Vandelay Industries",
        "stateOrRegion": "NY",
        "city": "Bronx",
        "countryCode": "US",
        "postalCode": "10451",
        "email": "shipper@example.com",
    },
    "shipTo": {
        "name": "AmazonShipping",
        "addressLine1": "417 Montgomery Street",
        "addressLine2": "5th Floor",
        "companyName": "AmazonShipping",
        "stateOrRegion": "CA",
        "city": "San Francisco",
        "countryCode": "US",
        "postalCode": "94104",
        "email": "recipient@example.com",
        "phoneNumber": "415-528-7555",
    },
    "packages": [
        {
            "dimensions": {
                "length": 9.0,
                "width": 6.0,
                "height": 2.0,
                "unit": "INCH",
            },
            "weight": {
                "value": 10.0,
                "unit": "POUND",
            },
            "insuredValue": {"value": 0.0, "unit": "USD"},
            "packageClientReferenceId": "1",
        }
    ],
    "channelDetails": {
        "channelType": "EXTERNAL",
    },
    "labelSpecifications": {
        "format": "PNG",
        "size": {
            "length": 6,
            "width": 4,
            "unit": "INCH",
        },
        "dpi": 300,
        "pageLayout": "DEFAULT",
        "needFileJoining": False,
        "requestedDocumentTypes": ["LABEL"],
    },
    "serviceSelection": {
        "serviceId": ["AMZN_US_STD"],
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "amazon_shipping",
        "carrier_name": "amazon_shipping",
        "docs": {"label": "base64_pdf_label"},
        "label_type": "PDF",
        "meta": {
            "carrier_id": "AMZN",
            "carrier_name": "Amazon",
            "currency": "USD",
            "service_id": "AMZN_US_STD",
            "service_name": "Amazon Shipping Standard",
            "shipment_id": "shipment-12345",
            "total_charge": 5.25,
            "tracking_numbers": ["1Z999AA10123456784"],
        },
        "shipment_identifier": "shipment-12345",
        "tracking_number": "1Z999AA10123456784",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "amazon_shipping",
        "carrier_name": "amazon_shipping",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


CancelShipmentRequestJSON = "shipment-12345"

ShipmentResponseJSON = """{
  "payload": {
    "shipmentId": "shipment-12345",
    "carrier": {
      "id": "AMZN",
      "name": "Amazon"
    },
    "service": {
      "id": "AMZN_US_STD",
      "name": "Amazon Shipping Standard"
    },
    "totalCharge": {
      "value": 5.25,
      "unit": "USD"
    },
    "packageDocumentDetails": [
      {
        "trackingId": "1Z999AA10123456784",
        "packageDocuments": [
          {
            "type": "LABEL",
            "format": "PNG",
            "contents": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
          }
        ]
      }
    ]
  }
}
"""
