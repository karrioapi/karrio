import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(
            **ReturnShipmentPayload
        )

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentRequest
        )
        serialized = request.serialize()

        # Verify the return service is set
        return_service = (
            serialized["ShipmentRequest"]["Shipment"].get("ReturnService")
        )
        print(return_service)
        self.assertIsNotNone(return_service)
        self.assertEqual(return_service["Code"], "5")

    @patch("karrio.mappers.ups.proxy.lib.request", return_value="{}")
    def test_create_return_shipment(self, http_mock):
        karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url, f"{gateway.settings.server_url}/api/shipments/v2409/ship"
        )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ReturnShipmentPayload = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "packaging_type": "ups_customer_supplied_package",
            "description": "Description",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
        }
    ],
    "service": "ups_next_day_air",
    "is_return": True,
    "payment": {"paid_by": "sender"},
    "reference": "Return Shipment Test",
}

ParsedReturnShipmentResponse = [
    {
        "carrier_name": "ups",
        "carrier_id": "ups",
        "tracking_number": "1ZXXXXXXXXXXXXXXXX",
        "shipment_identifier": "1ZXXXXXXXXXXXXXXXX",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "return_shipment": {
            "tracking_number": "1ZXXXXXXXXXXXXXXXX",
            "shipment_identifier": "1ZXXXXXXXXXXXXXXXX",
            "tracking_url": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZXXXXXXXXXXXXXXXX/trackdetails",
            "service": "ups_return_3_attempt",
            "meta": {"return_service_code": "5"},
        },
        "meta": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1ZXXXXXXXXXXXXXXXX/trackdetails",
            "tracking_numbers": ["1ZXXXXXXXXXXXXXXXX"],
        },
    },
    [],
]

ShipmentResponseJSON = """{
    "ShipmentResponse": {
        "Response": {
            "ResponseStatus": {
                "Code": "1",
                "Description": "Success"
            },
            "TransactionReference": {
                "CustomerContext": "Return Shipment Test"
            }
        },
        "ShipmentResults": {
            "ShipmentCharges": {
                "TransportationCharges": {
                    "CurrencyCode": "USD",
                    "MonetaryValue": "25.00"
                },
                "ServiceOptionsCharges": {
                    "CurrencyCode": "USD",
                    "MonetaryValue": "0.00"
                },
                "TotalCharges": {
                    "CurrencyCode": "USD",
                    "MonetaryValue": "25.00"
                }
            },
            "BillingWeight": {
                "UnitOfMeasurement": {
                    "Code": "LBS",
                    "Description": "Pounds"
                },
                "Weight": "10.0"
            },
            "ShipmentIdentificationNumber": "1ZXXXXXXXXXXXXXXXX",
            "PackageResults": [
                {
                    "TrackingNumber": "1ZXXXXXXXXXXXXXXXX",
                    "ServiceOptionsCharges": {
                        "CurrencyCode": "USD",
                        "MonetaryValue": "0.00"
                    },
                    "ShippingLabel": {
                        "ImageFormat": {
                            "Code": "PNG",
                            "Description": "PNG"
                        },
                        "GraphicImage": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
                    }
                }
            ]
        }
    }
}"""
