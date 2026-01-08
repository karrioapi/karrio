"""ParcelOne rate tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        serialized = request.serialize()

        self.assertDictEqual(serialized, RateRequestJSON)

    def test_get_rate(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_rate_error_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = RateErrorResponseJSON
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
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
    "services": ["parcelone_dhl_paket"],
}

RateRequestJSON = {
    "ShippingData": {
        "CEPID": "DHL",
        "ConsignerID": "TEST_CONSIGNER",
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
        "PrintLabel": 0,
        "ProductID": "PAKET",
        "ReturnCharges": 1,
        "ShipFromData": {
            "Name1": "Test Shipper",
            "ShipmentAddress": {
                "City": "Berlin",
                "Country": "DE",
                "PostalCode": "10115",
                "Street": "123 Teststrasse",
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
            },
        },
        "Software": "Karrio",
    }
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 4.99, "currency": "EUR", "name": "Base shipping"},
                {"amount": 1.0, "currency": "EUR", "name": "Fuel surcharge"},
            ],
            "meta": {"service_name": "parcelone_dhl_paket"},
            "service": "parcelone_dhl_paket",
            "total_charge": 5.99,
        }
    ],
    [],
]

ParsedRateErrorResponse = [
    [],
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "code": "E002",
            "details": {
                "shipment_id": "SHIP001",
            },
            "message": "Route not available",
        }
    ],
]


RateResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1
        },
        "TotalCharges": {
            "Value": "5.99",
            "Currency": "EUR"
        },
        "Charges": [
            {
                "Value": "4.99",
                "Currency": "EUR",
                "Description": "Base shipping"
            },
            {
                "Value": "1.00",
                "Currency": "EUR",
                "Description": "Fuel surcharge"
            }
        ]
    }
}"""

RateErrorResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 0,
            "ShipmentID": "SHIP001",
            "Errors": [
                {
                    "ErrorNo": "E002",
                    "Message": "Route not available"
                }
            ]
        }
    }
}"""
