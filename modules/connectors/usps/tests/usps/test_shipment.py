import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/label",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/label/794947717776",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "recipient": {
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "+1 123 456 7890",
        "state_code": "OK",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "carrier_service",
    "options": {
        "signature_required": True,
        "shipment_date": "2024-07-28",
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "docs": {"invoice": ANY, "label": ANY},
        "label_type": "PDF",
        "meta": {
            "SKU": "string",
            "labelBrokerID": "string",
            "postage": 0,
            "routingInformation": "string",
        },
        "shipment_identifier": "string",
        "tracking_number": "string",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = [
    {
        "fromAddress": {
            "ZIPPlus4": "29440",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "firstName": "Tall Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "imageInfo": {
            "imageType": "PDF",
            "labelType": "4X6LABEL",
            "receiptOption": "SEPARATE_PAGE",
        },
        "packageDescription": {
            "customerReference": [
                {"printReferenceNumber": True, "referenceNumber": "#Order 11111"}
            ],
            "destinationEntryFacilityType": "NONE",
            "dimensionsUOM": "in",
            "girth": 124.0,
            "height": 19.69,
            "inductionZIPCode": "29440",
            "length": 19.69,
            "mailClass": "carrier_service",
            "mailingDate": "2024-07-28",
            "processingCategory": "NON_MACHINABLE",
            "rateIndicator": "SP",
            "weight": 44.1,
            "weightUOM": "lb",
            "width": 4.72,
        },
        "senderAddress": {
            "ZIPPlus4": "29440",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "firstName": "Tall Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "toAddress": {
            "ZIPCode": "73108",
            "city": "Oklahoma City",
            "firm": "Horizon",
            "firstName": "Lina Smith",
            "ignoreBadAddress": True,
            "phone": "+1 123 456 7890",
            "secondaryAddress": "Apt 303",
            "streetAddress": "1309 S Agnew Avenue",
        },
    }
]

ShipmentCancelRequest = [{"trackingNumber": "794947717776"}]

ShipmentResponse = """{
  "labelMetadata": {
    "labelAddress": {
      "streetAddress": "string",
      "streetAddressAbbreviation": "string",
      "secondaryAddress": "string",
      "cityAbbreviation": "string",
      "city": "string",
      "state": "st",
      "ZIPCode": "string",
      "ZIPPlus4": "string",
      "urbanization": "string",
      "firstName": "string",
      "lastName": "string",
      "firm": "string",
      "phone": "string",
      "email": "user@example.com",
      "ignoreBadAddress": true
    },
    "routingInformation": "string",
    "trackingNumber": "string",
    "constructCode": "string",
    "SKU": "string",
    "postage": 0,
    "extraServices": [
      {
        "name": "string",
        "SKU": "string",
        "price": 0
      }
    ],
    "zone": "string",
    "commitment": {
      "name": "string",
      "scheduleDeliveryDate": "string"
    },
    "weightUOM": "string",
    "weight": 0,
    "dimensionalWeight": 0,
    "fees": [
      {
        "name": "string",
        "SKU": "string",
        "price": 0
      }
    ],
    "permitHolderName": "string",
    "inductionType": {},
    "labelBrokerID": "string",
    "links": [
      {
        "rel": ["string"],
        "title": "string",
        "href": "http://example.com",
        "method": "GET",
        "submissionMediaType": "string",
        "targetMediaType": "string"
      }
    ]
  },
  "returnLabelMetadata": {
    "labelAddress": {
      "streetAddress": "string",
      "streetAddressAbbreviation": "string",
      "secondaryAddress": "string",
      "cityAbbreviation": "string",
      "city": "string",
      "state": "st",
      "ZIPCode": "string",
      "ZIPPlus4": "string",
      "urbanization": "string",
      "firstName": "string",
      "lastName": "string",
      "firm": "string",
      "phone": "string",
      "email": "user@example.com",
      "ignoreBadAddress": true
    },
    "routingInformation": "string",
    "trackingNumber": "string",
    "SKU": "string",
    "postage": 0,
    "extraServices": [
      {
        "name": "string",
        "SKU": "string",
        "price": 0
      }
    ],
    "zone": "string",
    "weightUOM": "string",
    "weight": 0,
    "dimensionalWeight": 0,
    "fees": [
      {
        "name": "string",
        "SKU": "string",
        "price": 0
      }
    ],
    "labelBrokerID": "string",
    "links": [
      {
        "rel": ["string"],
        "title": "string",
        "href": "http://example.com",
        "method": "GET",
        "submissionMediaType": "string",
        "targetMediaType": "string"
      }
    ]
  },
  "labelImage": "string",
  "receiptImage": "string",
  "returnLabelImage": "string",
  "returnReceiptImage": "string"
}
"""

ShipmentCancelResponse = """{"ok": true}"""
