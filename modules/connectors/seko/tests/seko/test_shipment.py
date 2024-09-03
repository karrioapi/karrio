import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsShipping(unittest.TestCase):
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
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
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
        "carrier_id": "seko",
        "carrier_name": "seko",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "DeliveryReference": "OrderNumber123",
    "Reference2": "",
    "Reference3": "",
    "Origin": {
        "Id": 0,
        "Name": "OriginName",
        "Address": {
            "BuildingName": "",
            "StreetAddress": "285 Main Street",
            "Suburb": "GLENWOOD",
            "City": "NSW",
            "PostCode": "2768",
            "CountryCode": "AU",
        },
        "ContactPerson": "Origin contact name",
        "PhoneNumber": "02 9111 01101",
        "Email": "originemail@sekologistics.com",
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "RecipientTaxId": "123456",
    },
    "Destination": {
        "Id": 0,
        "Name": "Destination Name",
        "Address": {
            "BuildingName": "Markettown",
            "StreetAddress": "285 Coward Street",
            "Suburb": "TESBURY",
            "City": "VIC",
            "PostCode": "3260",
            "CountryCode": "AU",
        },
        "ContactPerson": "JOHN SMITH",
        "PhoneNumber": "02 9111 1111",
        "Email": "destinationemail@test.com",
        "DeliveryInstructions": "LEAVE AT FRONT DOOR",
        "RecipientTaxId": "123456",
        "SendTrackingEmail": "true",
    },
    "DangerousGoods": {
        "AdditionalHandlingInfo": "sample",
        "HazchemCode": "sample",
        "IsRadioActive": "false",
        "CargoAircraftOnly": "false",
        "IsDGLQ": "false",
        "TotalQuantity": 2,
        "TotalKg": 1.2,
        "SignOffName": "name",
        "SignOffRole": "dangerous goods officer",
        "LineItems": [
            {
                "HarmonizedCode": "sample",
                "Description": "sample",
                "ClassOrDivision": "sample",
                "UNorIDNo": "sample",
                "PackingGroup": "sample",
                "SubsidaryRisk": "sample",
                "Packing": "sample",
                "PackingInstr": "sample",
                "Authorization": "sample",
            }
        ],
    },
    "Commodities": [
        {
            "Description": "Food Bar",
            "Units": "1",
            "UnitValue": 50,
            "UnitKg": 0.6,
            "Currency": "USD",
            "Country": "AU",
            "IsDG": true,
            "itemSKU": "SKU123",
            "DangerousGoodsItem": {
                "HarmonizedCode": "sample",
                "Description": "sample",
                "ClassOrDivision": "sample",
                "UNorIDNo": "sample",
                "PackingGroup": "sample",
                "SubsidaryRisk": "sample",
                "Packing": "sample",
                "PackingInstr": "sample",
                "Authorization": "sample",
            },
        },
        {
            "Description": "Food Bar",
            "Units": "1",
            "UnitValue": 50,
            "UnitKg": 0.6,
            "Currency": "USD",
            "Country": "AU",
            "IsDG": true,
            "DangerousGoodsItem": {
                "Description": "sample",
                "ClassOrDivision": "sample",
                "UNorIDNo": "sample",
                "PackingGroup": "sample",
                "SubsidaryRisk": "sample",
                "Packing": "sample",
                "PackingInstr": "sample",
                "Authorization": "sample",
            },
        },
    ],
    "Packages": [
        {
            "Height": 1.0,
            "Length": 1.0,
            "Width": 1.0,
            "Kg": 5.0,
            "Name": "PARCEL",
            "Type": "Box",
            "OverLabelBarcode": "TEST0301201902",
        }
    ],
    "issignaturerequired": false,
    "DutiesAndTaxesByReceiver": false,
    "PrintToPrinter": true,
    "IncludeLineDetails": true,
    "Carrier": "Omni Parcel",
    "Service": "eCommerce Express Tracked",
    "CostCentreName": "mysite.com",
    "CodValue": 10.0,
    "TaxCollected": true,
    "AmountCollected": 10.0,
    "TaxIds": [
        {"IdType": "XIEORINumber", "IdNumber": "0121212112"},
        {"IdType": "IOSSNUMBER", "IdNumber": "0121212112"},
        {"IdType": "GBEORINUMBER", "IdNumber": "0121212112"},
        {"IdType": "VOECNUMBER", "IdNumber": "0121212112"},
        {"IdType": "VATNUMBER", "IdNumber": "0121212112"},
        {"IdType": "VENDORID", "IdNumber": "0121212113"},
        {"IdType": "NZIRDNUMBER", "IdNumber": "0121212115"},
        {"IdType": "SWISS VAT", "IdNumber": "CHE-123.456.789"},
        {"IdType": "OVRNUMBER", "IdNumber": "0121212112"},
        {"IdType": "EUEORINumber", "IdNumber": "0121212112"},
        {"IdType": "EUVATNumber", "IdNumber": "0121212112"},
        {"IdType": "LVGRegistrationNumber", "IdNumber": "0121212112"},
    ],
    "Outputs": ["LABEL_PDF_100X150"],
}


ShipmentCancelRequest = ["SSPOT014115", "SSPOT014114", "SSPOT014113", "SSPOT014112"]

ShipmentResponse = """{
  "CarrierId": 567,
  "CarrierName": "MyChildData",
  "IsFreightForward": false,
  "IsOvernight": false,
  "IsSaturdayDelivery": false,
  "IsRural": false,
  "HasTrackPaks": false,
  "Message": "Connote created and print queued.",
  "Errors": [
    {
      "Property": "Destination.Address.CountryCode",
      "Message": "CountryCode is required",
      "Key": "CountryCode",
      "Value": ""
    }
  ],
  "SiteId": 1153896,
  "Consignments": [
    {
      "Connote": "6994008906",
      "TrackingUrl": "http://track.omniparcel.com/1153896-6994008906",
      "Cost": 6.0,
      "CarrierType": 33,
      "IsSaturdayDelivery": false,
      "IsRural": false,
      "IsOvernight": false,
      "HasTrackPaks": false,
      "ConsignmentId": 5473553,
      "OutputFiles": {
        "LABEL_PDF_100X150": [
          "JVBERi0xLjQKJdP0zOEKMSAwIG9iago8PAovQ3JlYXRpb25EYXRlKEQ6MjAxNzAyMTMwOTA0MTkrMDU...."
        ]
      },
      "Items": [
        {
          "PartNo": 1,
          "TrackingNo": "699400890601",
          "Barcode": "019931265099999891699400890601",
          "InternalBarcode": "019931265099999891699400890601",
          "Charge": 6.54,
          "Charge_FAF": 0.0,
          "Charge_Rural": 0.0,
          "Charge_SatDel": 0.0,
          "Charge_Insurance": 0.0,
          "IsTrackPack": false,
          "BarcodeText": "699400890601",
          "TrackingBarcode": "019931265099999891699400890601",
          "TrackingBarcode2": "019931265099999891699400890601"
        }
      ]
    }
  ],
  "DestinationPort": "SYD",
  "Downloads": [],
  "CommodityChanges": [
    {
      "OriginalDescription": "OriginalDS1",
      "SuitableDescription": "SuitableDS1 - OriginalDS1",
      "OriginalHSCode": null,
      "SuitableHsCode": "1234567890"
    },
    {
      "OriginalDescription": "OriginalDS2",
      "SuitableDescription": "SuitableDS2 - OriginalDS2",
      "OriginalHSCode": null,
      "SuitableHsCode": "1234567890"
    }
  ],
  "CarrierType": 33,
  "AlertPath": null,
  "Notifications": [],
  "InvoiceResponse": "No Invoice found",
  "LogoPath": "http://cdn.omniparcel.com/images/aramex_logo_h50.png"
}
"""

ShipmentCancelResponse = """{
  "SSPOT014112": "Deleted",
  "SSPOT014113": "Deleted",
  "SSPOT014114": "Cannot be deleted. Already deleted.",
  "SSPOT014115": "Cannot be deleted. Already in transit."
}
"""
