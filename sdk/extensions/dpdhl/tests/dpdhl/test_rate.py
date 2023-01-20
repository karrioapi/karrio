import unittest
import karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from .fixture import gateway


class TestDPDHLRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {"postal_code": "00909", "country_code": "DE"},
    "recipient": {"postal_code": "00001", "country_code": "DE"},
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
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "currency": "EUR",
            "meta": {"service_name": "DHL Paket"},
            "service": "dpdhl_paket",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "currency": "EUR",
            "meta": {"service_name": "DHL Warenpost"},
            "service": "dpdhl_warenpost",
            "total_charge": 0.0,
        },
    ],
    [],
]
