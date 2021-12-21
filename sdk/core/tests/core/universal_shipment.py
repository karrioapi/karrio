import unittest
from unittest.mock import ANY
from purplship.core.utils import DP, Serializable
from purplship.core.models import ShipmentRequest
from purplship.universal.mappers.shipping_proxy import (
    ShippingMixinSettings,
    ShippingMixinProxy,
)
from purplship.universal.providers.shipping.shipment import parse_shipment_response


class TestUniversalShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.settings = ShippingMixinSettings(**settings_data)
        self.proxy = ShippingMixinProxy(self.settings)

    def test_shipment_request(self):
        ShipmentRequestData = Serializable(ShipmentRequest(**shipment_request_data))
        response_data = self.proxy.create_shipment(ShipmentRequestData)
        shipment = parse_shipment_response(response_data.deserialize(), self.settings)

        self.assertListEqual(
            DP.to_dict(shipment),
            ParsedShipmentResponse,
        )

    def test_multi_piece_shipment_request(self):
        ShipmentRequestData = Serializable(
            ShipmentRequest(
                **{
                    **shipment_request_data,
                    "parcels": [
                        shipment_request_data["parcels"][0],
                        shipment_request_data["parcels"][0],
                    ],
                }
            )
        )
        response_data = self.proxy.create_shipment(ShipmentRequestData)
        shipment = parse_shipment_response(response_data.deserialize(), self.settings)

        self.assertListEqual(
            DP.to_dict(shipment),
            ParsedMultiPieceShipmentResponse,
        )


if __name__ == "__main__":
    unittest.main()


settings_data = {
    "carrier_id": "universal",
    "services": [
        {
            "service_name": "Standard",
            "service_code": "carrier_standard",
            "cost": "10.00",
            "currency": "USD",
            "max_weight": 5.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
        },
        {
            "service_name": "Premium",
            "service_code": "carrier_premium",
            "cost": "15.00",
            "currency": "USD",
            "max_weight": 8.0,
            "weight_unit": "LB",
            "domicile": True,
            "international": False,
        },
    ],
}

shipment_request_data = {
    "service": "carrier_premium",
    "shipper": {"postal_code": "H8Z 2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "h8z2V4", "country_code": "CA"},
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
        }
    ],
}

ParsedShipmentResponse = [
    {
        "carrier_id": "universal",
        "label": ANY,
        "meta": {"service_name": "Premium"},
    },
    [],
]

ParsedMultiPieceShipmentResponse = [
    {
        "carrier_id": "universal",
        "label": ANY,
        "meta": {"service_name": "Premium"},
    },
    [],
]
