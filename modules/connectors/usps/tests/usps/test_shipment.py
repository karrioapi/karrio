import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

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

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
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
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
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
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {
    "imageInfo": {
        "imageType": "PDF",
        "labelType": "4X5LABEL",
        "shipInfo": True,
        "receiptOption": "SAME_PAGE",
        "suppressPostage": True,
        "suppressMailDate": True,
        "returnLabel": False,
    },
    "toAddress": {
        "streetAddress": "string",
        "secondaryAddress": "string",
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
        "ignoreBadAddress": True,
        "parcelLockerDelivery": False,
        "holdForPickup": False,
        "facilityId": "string",
    },
    "fromAddress": {
        "streetAddress": "string",
        "secondaryAddress": "string",
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
        "ignoreBadAddress": True,
    },
    "senderAddress": {
        "streetAddress": "string",
        "secondaryAddress": "string",
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
        "ignoreBadAddress": True,
        "platformUserId": "string",
    },
    "returnAddress": {
        "streetAddress": "string",
        "secondaryAddress": "string",
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
        "ignoreBadAddress": True,
    },
    "packageDescription": {
        "weightUOM": "lb",
        "weight": 0,
        "dimensionsUOM": "in",
        "length": 0,
        "height": 0,
        "width": 0,
        "girth": 0,
        "mailClass": "PARCEL_SELECT",
        "rateIndicator": "3D",
        "processingCategory": "LETTERS",
        "destinationEntryFacilityType": "NONE",
        "destinationEntryFacilityAddress": {
            "streetAddress": "string",
            "secondaryAddress": "string",
            "city": "string",
            "state": "st",
            "ZIPCode": "string",
            "ZIPPlus4": "string",
            "urbanization": "string",
        },
        "packageOptions": {
            "packageValue": 35,
            "nonDeliveryOption": "RETURN",
            "redirectAddress": {
                "streetAddress": "string",
                "secondaryAddress": "string",
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
                "ignoreBadAddress": True,
            },
            "contentType": "HAZMAT",
            "generateGXEvent": True,
            "containers": [{"containerID": "string", "sortType": "TRUCK_BEDLOAD"}],
            "ancillaryServiceEndorsements": "CHANGE_SERVICE_REQUESTED",
            "originalPackage": {
                "originalTrackingNumber": "4201234567899212391234567812345671",
                "originalConstructCode": "C01",
            },
        },
        "customerReference": [
            {"referenceNumber": "string", "printReferenceNumber": True}
        ],
        "extraServices": [365],
        "mailingDate": "2019-08-24",
        "carrierRelease": True,
        "physicalSignatureRequired": True,
        "inductionZIPCode": "string",
    },
    "customsForm": {
        "contentComments": "string",
        "restrictionType": "QUARANTINE",
        "restrictionComments": "string",
        "AESITN": "string",
        "invoiceNumber": "string",
        "licenseNumber": "string",
        "certificateNumber": "string",
        "customsContentType": "MERCHANDISE",
        "importersReference": "string",
        "importersContact": "string",
        "exportersReference": "string",
        "exportersContact": "string",
        "contents": [
            {
                "itemDescription": "Policy guidelines document",
                "itemQuantity": 1,
                "itemValue": 1,
                "itemTotalValue": 1,
                "weightUOM": "lb",
                "itemWeight": 1.0001,
                "itemTotalWeight": 1.0001,
                "HSTariffNumber": "string",
                "countryofOrigin": "string",
                "itemCategory": "string",
                "itemSubcategory": "string",
            }
        ],
    },
}

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

ShipmentCancelResponse = """"""
