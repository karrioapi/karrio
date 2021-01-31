import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Rating
from purplship.core.models import RateRequest
from tests.carrier.fixture import gateway


class TestCarrierRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequestXML)

    def test_get_rates(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("purplship.mappers.carrier.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedQuoteResponse))


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "residential": False,
    },
    "recipient": {
        "address_line1": "1 TEST ST",
        "city": "TORONTO",
        "company_name": "TEST ADDRESS",
        "phone_number": "4161234567",
        "postal_code": "M4X1W7",
        "state_code": "ON",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "services": ["carrier_ground"],
    "options": {
        "carrier_extra_care": True,
    },
}

ParsedQuoteResponse = [
    [],
    [],
]


RateRequestXML = """
"""

RateResponseXml = """
"""
