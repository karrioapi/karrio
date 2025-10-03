import unittest
from unittest.mock import ANY
from karrio.core.utils import DP, Serializable
from karrio.core.models import ShipmentRequest
from karrio.universal.mappers.shipping_proxy import (
    ShippingMixinSettings,
    ShippingMixinProxy,
)
from karrio.universal.providers.shipping.shipment import parse_shipment_response

import logging

logging.disable(logging.CRITICAL)


class TestUniversalShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = ShippingMixinSettings(**settings_data)
        self.proxy = ShippingMixinProxy(self.settings)

    def test_shipment_request(self):
        ShipmentRequestData = Serializable(ShipmentRequest(**shipment_request_data))
        response_data = self.proxy.create_shipment(ShipmentRequestData)
        shipment = parse_shipment_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(shipment),
            ParsedShipmentResponse,
        )

    def test_multi_piece_shipment_request(self):
        ShipmentRequestData = Serializable(
            ShipmentRequest(
                **{
                    **shipment_request_data,
                    "label_type": "PDF",
                    "parcels": [
                        shipment_request_data["parcels"][0],
                        shipment_request_data["parcels"][0],
                    ],
                }
            )
        )
        response_data = self.proxy.create_shipment(ShipmentRequestData)
        shipment = parse_shipment_response(response_data, self.settings)

        self.assertListEqual(
            DP.to_dict(shipment),
            ParsedMultiPieceShipmentResponse,
        )


if __name__ == "__main__":
    unittest.main()


settings_data = {
    "carrier_id": "custom-carrier",
    "services": [
        {
            "service_name": "Standard",
            "service_code": "carrier_standard",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 10.00}],
        },
        {
            "service_name": "Premium",
            "service_code": "carrier_premium",
            "currency": "USD",
            "max_weight": 8.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
            "zones": [{"rate": 15.00}],
        },
    ],
    "metadata": {
        "APP_ID": "00",
        "EXTENSION_DIGIT": "0",
        "GS1_PREFIX": "0099999000",
        "CHECK_DIGIT": "5",
    },
}

shipment_request_data = {
    "service": "carrier_premium",
    "label_type": "ZPL",
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "items": [
                {
                    "weight": 1.0,
                    "weight_unit": "LB",
                    "quantity": 1,
                    "title": "Item 1",
                    "sku": "SKU-1",
                    "metadata": {
                        "RFF_CN": "037-2332855",
                        "BGM": "040000000000016256",
                        "RFF_ON": "5424560",
                        "DEPT": "DBR128",
                        "CTL": "11253678",
                        "XXNC": "138039C01",
                        "NAD_UD": "570162",
                        "RFF_AJY": "907",
                        "RFF_AEM": "3901L",
                    },
                },
            ],
        }
    ],
}

ParsedShipmentResponse = [
    {
        "carrier_id": "custom-carrier",
        "carrier_name": "custom_carrier",
        "label_type": "ZPL",
        "shipment_identifier": ANY,
        "tracking_number": ANY,
        "docs": {"label": ANY},
        "meta": {
            "service_name": "Premium",
        },
    },
    [],
]

ParsedMultiPieceShipmentResponse = [
    {
        "carrier_id": "custom-carrier",
        "carrier_name": "custom_carrier",
        "label_type": "PDF",
        "docs": {"label": ANY},
        "meta": {
            "service_name": "Premium",
            "shipment_identifiers": ANY,
            "tracking_numbers": ANY,
        },
        "shipment_identifier": ANY,
        "tracking_number": ANY,
    },
    [],
]
