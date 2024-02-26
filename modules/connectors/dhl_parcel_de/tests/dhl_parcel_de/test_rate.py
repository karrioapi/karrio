import unittest
import karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from .fixture import gateway


class TestDHLParcelDERating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "recipient": {
        "address_line1": "Kurt-Schumacher-Str. 20",
        "street_number": "Apartment 107",
        "city": "Bonn",
        "country_code": "DE",
        "email": "maria@musterfrau.de",
        "person_name": "Maria Musterfrau",
        "postal_code": "53113",
        "phone_number": "+49 987654321",
    },
    "shipper": {
        "address_line1": "Sträßchensweg 10",
        "street_number": "2. Etage",
        "city": "Bonn",
        "country_code": "DE",
        "email": "max@mustermann.de",
        "person_name": "My Online Shop GmbH",
        "phone_number": "+49 123456789",
        "postal_code": "53113",
    },
    "parcels": [
        {
            "dimension_unit": "CM",
            "height": 10.0,
            "length": 20.0,
            "weight": 5,
            "weight_unit": "KG",
            "width": 15.0,
        }
    ],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "currency": "EUR",
            "meta": {"service_name": "DHL Paket"},
            "service": "dhl_parcel_de_paket",
            "total_charge": 0.0,
        }
    ],
    [],
]
