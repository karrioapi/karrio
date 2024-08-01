import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSAPIENTShipping(unittest.TestCase):
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
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
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

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "ShipmentInformation": {
        "ContentType": "NDX",
        "Action": "Process",
        "LabelFormat": "PDF",
        "ServiceCode": "OLA",
        "DescriptionOfGoods": "Clothing",
        "ShipmentDate": "2024-06-17",
        "CurrencyCode": "GBP",
        "WeightUnitOfMeasure": "KG",
        "DimensionsUnitOfMeasure": "MM",
        "ContainerId": "South East",
        "DeclaredWeight": 1.5,
        "BusinessTransactionType": "01",
    },
    "Shipper": {
        "Address": {
            "ContactName": "Jane Smith",
            "CompanyName": "Company & Co.",
            "ContactEmail": "email@server.com",
            "ContactPhone": "607723456789",
            "Line1": "Level 5",
            "Line2": "Hashmoore House",
            "Line3": "10 Sky Lane",
            "Town": "Leatherhead",
            "Postcode": "AA34 3AB",
            "County": "Surrey",
            "CountryCode": "GB",
        },
        "ShippingAccountId": "1991b077-3934-4efc-b9cb-2a916436d3ae",
        "ShippingLocationId": "f7f38476-3d11-4c8e-be61-20b158393401",
        "Reference1": "OrderRef56",
        "DepartmentNumber": "0123456789",
        "EoriNumber": "GB213456789000",
        "VatNumber": "GB213456789",
    },
    "Destination": {
        "Address": {
            "ContactName": "John Smith",
            "ContactEmail": "john.smith@example.com",
            "CompanyName": "Company & Co.",
            "ContactPhone": "07123456789",
            "Line1": "10 Sky Road",
            "Line2": "10 Sky Road",
            "Line3": "",
            "Town": "Sydney",
            "Postcode": "2000",
            "County": "NSW",
            "CountryCode": "AU",
        },
        "EoriNumber": "GB123456789000",
        "VatNumber": "GB123456789",
    },
    "CarrierSpecifics": {
        "ServiceLevel": "02",
        "EbayVtn": "ebay1234abc",
        "ServiceEnhancements": [
            {"Code": "CustomsEmail"},
            {"Code": "CustomsPhone"},
            {"Code": "Safeplace", "SafeplaceLocation": "Under the doormat"},
        ],
    },
    "Customs": {
        "ReasonForExport": "Sale Of Goods",
        "Incoterms": "DDU",
        "PreRegistrationNumber": "0123456789",
        "PreRegistrationType": "GST",
        "ShippingCharges": 55.82,
        "OtherCharges": 32,
        "QuotedLandedCost": 82.74,
        "InvoiceNumber": "INV-12345",
        "InvoiceDate": "2024-06-17",
        "ExportLicenceRequired": False,
        "Airn": "231.002.999-00",
    },
    "ReturnToSender": {
        "Address": {
            "ContactName": "Jane Smith",
            "CompanyName": "Company & Co.",
            "ContactEmail": "email@server.com",
            "ContactPhone": "07723456789",
            "Line1": "Level 5",
            "Line2": "Hashmoore House",
            "Line3": "10 Sky Lane",
            "Town": "Leatherhead",
            "Postcode": "AA34 3AB",
            "County": "Surrey",
            "CountryCode": "GB",
        }
    },
    "Packages": [
        {
            "PackageType": "Parcel",
            "PackageOccurrence": 1,
            "DeclaredWeight": 1.5,
            "DeclaredValue": 98.99,
            "Dimensions": {"Length": 40, "Width": 30, "Height": 20},
        }
    ],
    "Items": [
        {
            "SkuCode": "SKU123",
            "PackageOccurrence": 1,
            "Quantity": 1,
            "Description": "White Mens Large T-shirt",
            "Value": 19.99,
            "Weight": 0.5,
            "HSCode": "6109100010",
            "CountryOfOrigin": "CN",
        },
        {
            "SkuCode": "SKU456",
            "PackageOccurrence": 1,
            "Quantity": 2,
            "Description": "Black Mens Large Jumper",
            "Value": 32.99,
            "Weight": 0.3,
            "HSCode": "6110113000",
            "CountryOfOrigin": "CN",
        },
    ],
}

ShipmentCancelRequest = {"ShipmentId": "fa3bb603-2687-4b38-ba18-3264208446c6"}

ShipmentResponse = """{
  "Labels": "jVBERw0KGgoAAAANSUhEUgAA.....A4QAAAXcCAYAAAB6Q0CbAAAAAXNSR0IArs4",
  "LabelFormat": "PDF",
  "Packages": [
    {
      "CarrierDetails": {
        "UniqueId": "3A07033860010000B2268"
      },
      "ShipmentId": "fa3bb603-2687-4b38-ba18-3264208446c6",
      "PackageOccurrence": 1,
      "TrackingNumber": "TT123456785GB",
      "CarrierTrackingUrl": "https://www.royalmail.com/track-your-item#/tracking-results/TT123456785GB"
    }
  ]
}
"""

ShipmentCancelResponse = """{"ok": true}"""
