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
                f"{gateway.settings.server_url}/labels/printshipment",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels/delete",
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
    "service": "seko_ecommerce_express_tracked",
    "shipper": {
        "company_name": "OriginName",
        "address_line1": "285 Main Street",
        "city": "GLENWOOD",
        "postal_code": "2768",
        "country_code": "AU",
        "person_name": "Origin contact name",
        "state_code": "NSW",
        "email": "originemail@sekologistics.com",
        "phone_number": "02 9111 01101",
        "state_tax_id": "123456",
    },
    "recipient": {
        "company_name": "Destination Name",
        "address_line1": "285 Coward Street",
        "city": "TESBURY",
        "postal_code": "3260",
        "country_code": "AU",
        "person_name": "JOHN SMITH",
        "state_code": "VIC",
        "email": "destinationemail@test.com",
        "phone_number": "02 9111 1111",
        "state_tax_id": "123456",
    },
    "parcels": [
        {
            "height": 1.0,
            "length": 1.0,
            "weight": 5.0,
            "width": 1.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "reference_number": "TEST0301201902",
            "packaging_type": "small_box",
            "description": "PARCEL",
        }
    ],
    "options": {
        "origin_instructions": "Desinationdeliveryinstructions",
        "destination_instructions": "LEAVE AT FRONT DOOR",
        "seko_send_tracking_email": True,
        "seko_carrier": "Omni Parcel",
        "signature_required": False,
        "seko_amount_collected": 10.0,
        "cash_on_delivery": 10.0,
        "currency": "USD",
    },
    "reference": "OrderNumber123",
    "customs": {
        "commodities": [
            {
                "description": "Food Bar",
                "quantity": 1,
                "value_amount": 50,
                "value_currency": "USD",
                "weight": 0.6,
                "origin_country": "AU",
                "sku": "SKU123",
            },
            {
                "description": "Food Bar",
                "quantity": 1,
                "value_amount": 50,
                "value_currency": "USD",
                "weight": 0.6,
                "origin_country": "AU",
            },
        ],
        "options": {
            "XIEORINumber": "0121212112",
            "IOSSNUMBER": "0121212112",
            "GBEORINUMBER": "0121212112",
            "VOECNUMBER": "0121212112",
            "VATNUMBER": "0121212112",
            "VENDORID": "0121212113",
            "NZIRDNUMBER": "0121212115",
            "SWISS_VAT": "CHE-123.456.789",
            "OVRNUMBER": "0121212112",
            "EUEORINumber": "0121212112",
            "EUVATNumber": "0121212112",
            "LVGRegistrationNumber": "0121212112",
        },
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
    "options": {
        "shipment_identifiers": [
            "SSPOT014115",
            "SSPOT014114",
            "SSPOT014113",
            "SSPOT014112",
        ]
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "seko",
        "carrier_name": "seko",
        "docs": {
            "label": "JVBERi0xLjcKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL01lZGlhQm94IFsgMCAwIDMuNiAzLjYgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA2IDAgUgovVHJpbUJveCBbIDAgMCAzLjYgMy42IF0KL0JsZWVkQm94IFsgMCAwIDMuNiAzLjYgXQovUGFyZW50IDEgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggNzEKPj4Kc3RyZWFtCnjaM1QwAEJdQyBhrGemkJzLVchloGduChaGM8DChVyGCiBYlM6ln2ioZ6CQXswFkjTRswDjolSucK48dKE0rkAQBAAu7xTjCmVuZHN0cmVhbQplbmRvYmoKNiAwIG9iago8PAovRXh0R1N0YXRlIDw8Ci9hMS4wIDw8Ci9jYSAxCj4+Cj4+Ci9YT2JqZWN0IDw8Cj4+Ci9QYXR0ZXJuIDw8Cj4+Ci9TaGFkaW5nIDw8Cj4+Ci9Gb250IDcgMCBSCj4+CmVuZG9iago3IDAgb2JqCjw8Cj4+CmVuZG9iagp4cmVmCjAgOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA3NCAwMDAwMCBuIAowMDAwMDAwMTE0IDAwMDAwIG4gCjAwMDAwMDAxNjMgMDAwMDAgbiAKMDAwMDAwMDMyMCAwMDAwMCBuIAowMDAwMDAwNDYyIDAwMDAwIG4gCjAwMDAwMDA1NzUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA4Ci9Sb290IDMgMCBSCi9JbmZvIDIgMCBSCj4+CnN0YXJ0eHJlZgo1OTYKJSVFT0YK"
        },
        "label_type": "PDF",
        "meta": {
            "CarrierId": 567,
            "CarrierName": "MyChildData",
            "ConsignmentId": 5473553,
            "ConsignmentIds": [5473553],
            "SiteId": 1153896,
            "TrackingUrls": ["http://track.omniparcel.com/1153896-6994008906"],
            "carrier_tracking_link": "http://track.omniparcel.com/1153896-6994008906",
        },
        "shipment_identifier": 5473553,
        "tracking_number": "6994008906",
    },
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "Error",
            "details": {
                "Key": "CountryCode",
                "Property": "Destination.Address.CountryCode",
            },
            "message": "CountryCode is required",
        }
    ],
]

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "seko",
        "carrier_name": "seko",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "Error",
            "details": {
                "ConsignmentId": "SSPOT014114",
            },
            "message": "Cannot be deleted. Already deleted.",
        },
        {
            "carrier_id": "seko",
            "carrier_name": "seko",
            "code": "Error",
            "details": {
                "ConsignmentId": "SSPOT014115",
            },
            "message": "Cannot be deleted. Already in transit.",
        },
    ],
]


ShipmentRequest = {
    "DeliveryReference": "OrderNumber123",
    "Origin": {
        "Name": "OriginName",
        "Address": {
            "City": "NSW",
            "StreetAddress": "285 Main Street",
            "PostCode": "2768",
            "CountryCode": "AU",
            "Suburb": "GLENWOOD",
        },
        "ContactPerson": "Origin contact name",
        "PhoneNumber": "02 9111 01101",
        "Email": "originemail@sekologistics.com",
        "DeliveryInstructions": "Desinationdeliveryinstructions",
        "RecipientTaxId": "123456",
    },
    "Destination": {
        "Name": "Destination Name",
        "Address": {
            "StreetAddress": "285 Coward Street",
            "City": "VIC",
            "Suburb": "TESBURY",
            "PostCode": "3260",
            "CountryCode": "AU",
            "Suburb": "TESBURY",
        },
        "ContactPerson": "JOHN SMITH",
        "PhoneNumber": "02 9111 1111",
        "Email": "destinationemail@test.com",
        "DeliveryInstructions": "LEAVE AT FRONT DOOR",
        "RecipientTaxId": "123456",
        "SendTrackingEmail": True,
    },
    "Commodities": [
        {
            "Description": "Food Bar",
            "Units": 1,
            "UnitValue": 50,
            "UnitKg": 0.6,
            "Currency": "USD",
            "Country": "AU",
            "itemSKU": "SKU123",
            "HarmonizedCode": "0000.00.00",
        },
        {
            "Description": "Food Bar",
            "Units": 1,
            "UnitValue": 50,
            "UnitKg": 0.6,
            "Currency": "USD",
            "Country": "AU",
            "HarmonizedCode": "0000.00.00",
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
    "issignaturerequired": False,
    "DutiesAndTaxesByReceiver": False,
    "PrintToPrinter": True,
    "IncludeLineDetails": True,
    "Carrier": "Omni Parcel",
    "Service": "eCommerce Express Tracked",
    "CostCentreName": "mysite.com",
    "CodValue": 10.0,
    "TaxCollected": True,
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
          "JVBERi0xLjcKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL01lZGlhQm94IFsgMCAwIDMuNiAzLjYgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA2IDAgUgovVHJpbUJveCBbIDAgMCAzLjYgMy42IF0KL0JsZWVkQm94IFsgMCAwIDMuNiAzLjYgXQovUGFyZW50IDEgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggNzEKPj4Kc3RyZWFtCnjaM1QwAEJdQyBhrGemkJzLVchloGduChaGM8DChVyGCiBYlM6ln2ioZ6CQXswFkjTRswDjolSucK48dKE0rkAQBAAu7xTjCmVuZHN0cmVhbQplbmRvYmoKNiAwIG9iago8PAovRXh0R1N0YXRlIDw8Ci9hMS4wIDw8Ci9jYSAxCj4+Cj4+Ci9YT2JqZWN0IDw8Cj4+Ci9QYXR0ZXJuIDw8Cj4+Ci9TaGFkaW5nIDw8Cj4+Ci9Gb250IDcgMCBSCj4+CmVuZG9iago3IDAgb2JqCjw8Cj4+CmVuZG9iagp4cmVmCjAgOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA3NCAwMDAwMCBuIAowMDAwMDAwMTE0IDAwMDAwIG4gCjAwMDAwMDAxNjMgMDAwMDAgbiAKMDAwMDAwMDMyMCAwMDAwMCBuIAowMDAwMDAwNDYyIDAwMDAwIG4gCjAwMDAwMDA1NzUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA4Ci9Sb290IDMgMCBSCi9JbmZvIDIgMCBSCj4+CnN0YXJ0eHJlZgo1OTYKJSVFT0YK"
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
