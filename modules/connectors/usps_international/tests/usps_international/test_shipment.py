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
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/international-label",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/international-label/794947717776",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps_international.proxy.lib.request") as mock:
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
        "company_name": "Coffee Five",
        "address_line1": "R. da Quitanda, 86 - quiosque 01",
        "city": "Centro",
        "postal_code": "29440",
        "country_code": "BR",
        "person_name": "John",
        "phone_number": "8005554526",
        "state_code": "Rio de Janeiro",
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
    "service": "usps_global_express_guaranteed_non_document_non_rectangular",
    "customs": {
        "content_type": "merchandise",
        "incoterm": "DDU",
        "invoice": "INV-040903",
        "commodities": [
            {
                "weight": 2,
                "weight_unit": "KG",
                "quantity": 1,
                "hs_code": "XXXXX0000123",
                "value_amount": 30,
                "value_currency": "USD",
                "origin_country": "US",
            }
        ],
        "duty": {
            "paid_by": "recipient",
            "currency": "USD",
            "declared_value": 60,
        },
        "certify": True,
        "signer": "Admin",
        "options": {
            "license_number": "LIC-24356879",
            "certificate_number": "CERT-97865342",
        },
    },
    "options": {"shipment_date": "2021-05-15", "insurance": 75.0},
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {
            "SKU": "string",
            "postage": 0,
        },
        "shipment_identifier": "string",
        "tracking_number": "string",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = [
    {
        "customsForm": {
            "certificateNumber": "CERT-97865342",
            "contents": [
                {
                    "HSTariffNumber": "XXXXX0000123",
                    "countryofOrigin": "US",
                    "itemQuantity": 1,
                    "itemTotalValue": 30,
                    "itemTotalWeight": 4.41,
                    "itemValue": 30,
                    "itemWeight": 4.41,
                    "weightUOM": "lb",
                }
            ],
            "customsContentType": "MERCHANDISE",
            "invoiceNumber": "INV-040903",
            "licenseNumber": "LIC-24356879",
        },
        "fromAddress": {
            "ZIPPlus4": "29440",
            "city": "Georgetown",
            "firm": "ABC Corp.",
            "firstName": "Tall Tom",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "1098 N Fraser Street",
        },
        "imageInfo": {"imageType": "PDF", "labelType": "4X6LABEL"},
        "packageDescription": {
            "customerReference": [{"referenceNumber": "#Order 11111"}],
            "destinationEntryFacilityType": "NONE",
            "dimensionsUOM": "in",
            "extraServices": [930],
            "girth": {
                "_side1": {"_unit": "CM", "_value": 12},
                "_side2": {"_unit": "CM", "_value": 50},
                "_side3": {"_unit": "CM", "_value": 50},
            },
            "height": 19.69,
            "length": 19.69,
            "mailClass": "usps_global_express_guaranteed_non_document_non_rectangular",
            "mailingDate": "2021-05-15",
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
            "ZIPCode": "29440",
            "city": "Centro",
            "firm": "Coffee Five",
            "firstName": "John",
            "ignoreBadAddress": True,
            "phone": "8005554526",
            "streetAddress": "R. da Quitanda, 86 - quiosque 01",
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
      "postalCode": "string",
      "province": "string",
      "country": "string",
      "countryISOAlpha2Code": "string",
      "firstName": "string",
      "lastName": "string",
      "firm": "string",
      "phone": "string"
    },
    "internationalTrackingNumber": "string",
    "constructCode": "string",
    "SKU": "string",
    "postage": 0,
    "extraServices": [
      {
        "serviceID": "string",
        "serviceName": "string",
        "price": 0
      }
    ],
    "internationalPriceGroup": "string",
    "weightUOM": "lb",
    "weight": 5,
    "dimensionalWeight": "string",
    "fees": [
      {
        "name": "string",
        "SKU": "string",
        "price": 0
      }
    ],
    "labelBrokerID": "string"
  },
  "labelImage": "string"
}
"""

ShipmentCancelResponse = """{"ok": true}"""
