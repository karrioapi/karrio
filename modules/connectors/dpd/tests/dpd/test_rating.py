import unittest
import karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from .fixture import gateway


class TestDPDRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "options": {
        "currency": "EUR",
        "declared_value": 174.8,
    },
    "parcels": [
        {
            "dimension_unit": "IN",
            "height": 6,
            "is_document": False,
            "length": 24,
            "packaging_type": "your_packaging",
            "weight": 15,
            "weight_unit": "KG",
            "width": 14,
        }
    ],
    "recipient": {
        "address_line1": "Teststraat 5",
        "city": "Mechelen",
        "country_code": "BE",
        "email": "scgmoutboundops@xpo.com",
        "person_name": "Receivers NV",
        "phone_number": "+1 855-654-7157",
        "postal_code": "2800",
        "residential": False,
    },
    "shipper": {
        "address_line1": "Egide Walschaertsstraat 20",
        "city": "Mechelen",
        "country_code": "BE",
        "person_name": "Senders NV",
        "phone_number": "+1 403-329-8801",
        "postal_code": "2800",
        "residential": False,
    },
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "currency": "EUR",
            "meta": {"service_name": "DPD Express 10h"},
            "service": "dpd_express_10h",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "currency": "EUR",
            "meta": {"service_name": "DPD Express 12h"},
            "service": "dpd_express_12h",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "currency": "EUR",
            "meta": {"service_name": "DPD Express 18h Guarantee"},
            "service": "dpd_express_18h_guarantee",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "currency": "EUR",
            "meta": {"service_name": "DPD B2B MSG option"},
            "service": "dpd_express_b2b_predict",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "currency": "EUR",
            "meta": {"service_name": "CL"},
            "service": "dpd_cl",
            "total_charge": 0.0,
        },
    ],
    [],
]
