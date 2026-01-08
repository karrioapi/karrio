"""ParcelOne shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = request.serialize()

        self.assertDictEqual(serialized, ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertDictEqual(request.serialize(), ShipmentCancelRequestJSON)

    def test_create_shipment(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment/TrackingID/123456789012",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_error_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentErrorResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentErrorResponse
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseJSON
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
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "email": "shipper@test.com",
        "phone_number": "+49301234567",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
        "email": "recipient@test.com",
        "phone_number": "+498912345678",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
            "length": 30.0,
            "width": 20.0,
            "height": 15.0,
            "dimension_unit": "CM",
        }
    ],
    "service": "parcelone_dhl_paket",
}

ShipmentCancelPayload = {
    "shipment_identifier": "123456789012",
}

ShipmentRequestJSON = {
    "ShippingData": {
        "CEPID": "DHL",
        "ConsignerID": "TEST_CONSIGNER",
        "LabelFormat": {
            "Size": "A6",
            "Type": "PDF",
        },
        "MandatorID": "TEST_MANDATOR",
        "Packages": [
            {
                "PackageDimensions": {
                    "Height": "15.0",
                    "Length": "30.0",
                    "Width": "20.0",
                },
                "PackageRef": "1",
                "PackageWeight": {
                    "Unit": "kg",
                    "Value": "5.0",
                },
            }
        ],
        "PrintDocuments": 0,
        "PrintLabel": 1,
        "ProductID": "PAKET",
        "ReturnShipmentIndicator": 0,
        "ShipFromData": {
            "Name1": "Test Shipper",
            "ShipmentAddress": {
                "City": "Berlin",
                "Country": "DE",
                "PostalCode": "10115",
                "Street": "123 Teststrasse",
                "Streetno": "123",
            },
            "ShipmentContact": {
                "Email": "shipper@test.com",
                "Phone": "+49301234567",
            },
        },
        "ShipToData": {
            "Name1": "Test Recipient",
            "PrivateAddressIndicator": 0,
            "ShipmentAddress": {
                "City": "Munich",
                "Country": "DE",
                "PostalCode": "80331",
                "Street": "456 Empfangerweg",
                "Streetno": "456",
            },
            "ShipmentContact": {
                "Email": "recipient@test.com",
                "Phone": "+498912345678",
            },
        },
        "Software": "Karrio",
    }
}

ShipmentCancelRequestJSON = {
    "ref_field": "TrackingID",
    "ref_value": "123456789012",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MKMSAwIG9iag=="},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://tracking.parcel.one/?trackingNumber=123456789012",
            "currency": "EUR",
            "shipment_id": "SHIP001",
            "total_charge": 5.99,
            "tracking_numbers": ["123456789012"],
        },
        "shipment_identifier": "SHIP001",
        "tracking_number": "123456789012",
    },
    [],
]

ParsedShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "code": "E001",
            "details": {
                "shipment_id": "SHIP001",
                "tracking_id": "123456789012",
            },
            "message": "Invalid postal code",
        }
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "SHIP001",
            "TrackingID": "123456789012"
        },
        "PackageResults": [
            {
                "PackageID": "PKG001",
                "TrackingID": "123456789012",
                "Label": "JVBERi0xLjQKJeLjz9MKMSAwIG9iag=="
            }
        ],
        "TotalCharges": {
            "Value": "5.99",
            "Currency": "EUR"
        },
        "LabelsAvailable": 1
    }
}"""

ShipmentErrorResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 0,
            "ShipmentID": "SHIP001",
            "TrackingID": "123456789012",
            "Errors": [
                {
                    "ErrorNo": "E001",
                    "Message": "Invalid postal code"
                }
            ]
        }
    }
}"""

ShipmentCancelResponseJSON = """{
    "success": 1,
    "results": {
        "Success": 1,
        "ShipmentID": "SHIP001",
        "TrackingID": "123456789012"
    }
}"""
