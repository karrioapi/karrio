import unittest
import karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from .fixture import gateway


class TestGenericRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {"postal_code": "11111", "country_code": "US"},
    "recipient": {"postal_code": "11111", "country_code": "US"},
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
    "services": [],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "custom-carrier",
            "carrier_name": "custom_carrier",
            "currency": "USD",
            "meta": {"service_name": "Standard Service"},
            "service": "standard_service",
            "total_charge": 100.0,
        }
    ],
    [],
]
