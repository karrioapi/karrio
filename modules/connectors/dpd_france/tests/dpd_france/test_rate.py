"""DPD France rating tests (universal rate-sheet provider)."""

import unittest

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from karrio.providers.dpd_france import units

from .fixture import gateway


class TestDPDFranceRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_default_services_loaded(self):
        services = units.DEFAULT_SERVICES
        self.assertEqual(len(services), 6)
        codes = [s.service_code for s in services]
        self.assertEqual(
            sorted(codes),
            sorted(
                [
                    "dpd_france_classic",
                    "dpd_france_predict",
                    "dpd_france_medical",
                    "dpd_france_relais_pickup_consigne",
                    "dpd_france_reverse_pickup",
                    "dpd_france_secure",
                ]
            ),
        )

    def test_parse_domestic_rate_response(self):
        request = models.RateRequest(**DomesticRatePayload)
        parsed = karrio.Rating.fetch(request).from_(gateway).parse()
        self.assertListEqual(lib.to_dict(parsed), ParsedDomesticRateResponse)

    def test_parse_international_rate_response(self):
        request = models.RateRequest(**InternationalRatePayload)
        parsed = karrio.Rating.fetch(request).from_(gateway).parse()
        self.assertListEqual(lib.to_dict(parsed), ParsedInternationalRateResponse)

    def test_parse_over_weight_rate_response(self):
        # 50kg exceeds the 30kg max — universal provider filters all services out
        request = models.RateRequest(**OverWeightRatePayload)
        parsed = karrio.Rating.fetch(request).from_(gateway).parse()
        self.assertListEqual(lib.to_dict(parsed), ParsedOverWeightRateResponse)


if __name__ == "__main__":
    unittest.main()


DomesticRatePayload = {
    "shipper": {
        "address_line1": "28 rue du Clair Bocage",
        "city": "La Seyne-sur-mer",
        "postal_code": "83500",
        "country_code": "FR",
    },
    "recipient": {
        "address_line1": "72 rue Reine Elisabeth",
        "city": "Menton",
        "postal_code": "06500",
        "country_code": "FR",
    },
    "parcels": [{"weight": 3.0, "weight_unit": "KG"}],
}

InternationalRatePayload = {
    "shipper": {
        "address_line1": "1 rue de Paris",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
    },
    "recipient": {
        "address_line1": "Friedrichstr. 1",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
    "parcels": [{"weight": 3.0, "weight_unit": "KG"}],
}

OverWeightRatePayload = {
    "shipper": {
        "address_line1": "1 rue",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
    },
    "recipient": {
        "address_line1": "2 rue",
        "city": "Lyon",
        "postal_code": "69001",
        "country_code": "FR",
    },
    "parcels": [{"weight": 50.0, "weight_unit": "KG"}],
}


def _domestic_rate(service: str, name: str, transit: int) -> dict:
    return {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "currency": "EUR",
        "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
        "meta": {
            "service_name": name,
            "shipping_charges": 0.0,
            "shipping_currency": "EUR",
        },
        "service": service,
        "total_charge": 0.0,
        "transit_days": transit,
    }


ParsedDomesticRateResponse = [
    [
        _domestic_rate("dpd_france_classic", "DPD Classic", 1),
        _domestic_rate("dpd_france_predict", "DPD Predict", 1),
        _domestic_rate("dpd_france_medical", "DPD Medical", 1),
        _domestic_rate("dpd_france_relais_pickup_consigne", "DPD Relais Pickup & Consigne", 2),
        _domestic_rate("dpd_france_reverse_pickup", "DPD Reverse at Pickup shop", 2),
        _domestic_rate("dpd_france_secure", "DPD Secure", 1),
    ],
    [],
]

ParsedInternationalRateResponse = [
    [
        _domestic_rate("dpd_france_classic", "DPD Classic", 2),
        _domestic_rate("dpd_france_predict", "DPD Predict", 2),
    ],
    [],
]

ParsedOverWeightRateResponse = [[], []]
