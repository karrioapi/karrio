import unittest
import karrio
from unittest.mock import ANY

from karrio.providers.generic.units import SAMPLE_SHIPMENT_REQUEST
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest
from .fixture import gateway


class TestGenericShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**SAMPLE_SHIPMENT_REQUEST)

    def test_parse_rate_response(self):
        parsed_response = (
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
        )

        self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ParsedShipmentResponse = [
    {
        "carrier_id": "custom-carrier",
        "carrier_name": "custom_carrier",
        "label_type": "ZPL",
        "docs": {"label": ANY},
        "meta": {"service_name": "carrier_premium"},
        "shipment_identifier": "2975565",
        "tracking_number": "2975565",
    },
    [],
]
