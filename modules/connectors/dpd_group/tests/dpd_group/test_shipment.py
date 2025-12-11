"""DPD Group carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestDPDGroupShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_group.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "Main Street",
        "street_number": "42",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "person_name": "John Sender",
        "company_name": "Sender Corp",
        "phone_number": "+49301234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Secondary Road",
        "street_number": "88",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
        "person_name": "Jane Receiver",
        "company_name": "Receiver Inc",
        "phone_number": "+33123456789",
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 3.0,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Electronic equipment",
        }
    ],
    "service": "dpd_group_classic",
    "reference": "SHIP123456",
}

ShipmentRequest = {
    "numberOfParcels": "1",
    "shipmentInfos": {
        "productCode": "101",
        "shipmentId": "SHIP123456",
        "weight": "3000",
        "dimensions": {"length": 30, "width": 20, "height": 15},
    },
    "sender": {
        "customerInfos": {
            "customerID": "123456789",
            "customerAccountNumber": "ACC123456",
        },
        "address": {
            "companyName": "Sender Corp",
            "name1": "John Sender",
            "street": "Main Street",
            "houseNumber": "42",
            "zipCode": "10115",
            "city": "Berlin",
            "country": "DE",
        },
        "contact": {"phone1": "+49301234567", "email": "sender@example.com"},
    },
    "receiver": {
        "address": {
            "name1": "Jane Receiver",
            "companyName": "Receiver Inc",
            "street": "Secondary Road",
            "houseNumber": "88",
            "zipCode": "75001",
            "city": "Paris",
            "country": "FR",
        },
        "contact": {"phone1": "+33123456789", "email": "receiver@example.com"},
    },
    "parcel": [
        {
            "parcelInfos": {
                "weight": 3000,
                "dimensions": {"length": 30, "width": 20, "height": 15},
            },
            "parcelContent": "Electronic equipment",
        }
    ],
}

ShipmentResponse = """{
  "shipmentId": "SHIP123456",
  "parcelIds": ["0987654321"],
  "networkShipmentId": "NET123456",
  "networkParcelIds": ["0987654321"],
  "parcelBarcodes": [
    {
      "parcel": "0987654321",
      "barcode": "0987654321000",
      "reference": "REF001"
    }
  ],
  "label": {
    "base64Data": "JVBERi0xLjQKJeLjz9MNCg==",
    "media-type": "application/pdf"
  }
}"""

ErrorResponse = """{
  "errorCode": "ERR001",
  "errorMessage": "Invalid shipment data",
  "errorOrigin": "META-API"
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "dpd_group",
        "carrier_name": "dpd_group",
        "tracking_number": "0987654321",
        "shipment_identifier": "SHIP123456",
        "label_type": "PDF",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MNCg=="},
        "meta": {
            "network_shipment_id": "NET123456",
            "network_parcel_ids": ["0987654321"],
            "parcel_barcodes": [
                {
                    "parcel": "0987654321",
                    "barcode": "0987654321000",
                    "reference": "REF001",
                }
            ],
            "tracking_url": "https://www.dpdgroup.com/tracking?parcelNumber=0987654321",
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_group",
            "carrier_name": "dpd_group",
            "code": "ERR001",
            "message": "Invalid shipment data",
            "details": {"errorOrigin": "META-API"},
        }
    ],
]
