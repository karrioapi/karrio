"""ParcelOne rate tests.

Rating is CSV-driven (RatingMixinProxy + services.csv).
Rates are 0.0 placeholder pending an authoritative rate card from ParcelOne.
No mock needed — universal_provider reads the local CSV directly.
"""

import unittest

import karrio.lib as lib
import karrio.sdk as karrio
from karrio.core.models import RateRequest
from karrio.providers.parcelone import units

from .fixture import gateway


class TestParcelOneRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


class TestParcelOneDefaultServices(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        self.assertGreater(len(self.services), 0)
        service_codes = [s.service_code for s in self.services]
        self.assertIn("parcelone_pa1_basic", service_codes)
        self.assertIn("parcelone_pa1_basicL", service_codes)
        self.assertIn("parcelone_pa1_eco", service_codes)
        self.assertIn("parcelone_pa1_ecoL", service_codes)
        self.assertIn("parcelone_dhl_101", service_codes)
        self.assertIn("parcelone_dhl_5302", service_codes)
        self.assertIn("parcelone_ups_11", service_codes)
        self.assertIn("parcelone_ups_07", service_codes)
        self.assertIn("parcelone_ups_65", service_codes)

    def test_all_services_have_zones(self):
        for service in self.services:
            self.assertGreater(
                len(service.zones),
                0,
                f"Service {service.service_code} should have zones",
            )
            for zone in service.zones:
                self.assertIsNotNone(zone.rate)
                self.assertGreaterEqual(zone.rate, 0)

    def test_domestic_pa1_basic_structure(self):
        pa1_basic = next((s for s in self.services if s.service_code == "parcelone_pa1_basic"), None)
        self.assertIsNotNone(pa1_basic)
        self.assertTrue(pa1_basic.domicile)
        self.assertEqual(pa1_basic.currency, "EUR")

    def test_pa1_basic_germany_zone_rate(self):
        pa1_basic = next((s for s in self.services if s.service_code == "parcelone_pa1_basic"), None)
        de_zone = next(
            (z for z in pa1_basic.zones if z.country_codes and "DE" in z.country_codes),
            None,
        )
        self.assertIsNotNone(de_zone)
        self.assertEqual(de_zone.rate, 0.0)


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {
        "person_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "12345",
        "country_code": "DE",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
    },
    "parcels": [
        {
            "weight": 1.5,
            "weight_unit": "KG",
            "length": 30.0,
            "width": 20.0,
            "height": 15.0,
            "dimension_unit": "CM",
        }
    ],
}


def _rate(service, service_name, transit_days):
    return {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "currency": "EUR",
        "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
        "meta": {"service_name": service_name, "shipping_charges": 0.0, "shipping_currency": "EUR"},
        "service": service,
        "total_charge": 0.0,
        "transit_days": transit_days,
    }


ParsedRateResponse = [
    [
        _rate("parcelone_pa1_basic", "Parcel.One Basic", 2),
        _rate("parcelone_pa1_basicL", "Letter Basic", 2),
        _rate("parcelone_pa1_eco", "Parcel.One Eco", 3),
        _rate("parcelone_pa1_ecoL", "Letter Eco", 3),
        _rate("parcelone_pa1_plus", "Parcel Plus", 1),
        _rate("parcelone_pa1_plusL", "Parcel Plus L", 1),
        _rate("parcelone_pa1_plusZ", "Parcel Plus Z", 1),
        _rate("parcelone_dhl_101", "DHL National", 1),
        _rate("parcelone_dhl_5301", "DHL Weltpaket Premium", 1),
        _rate("parcelone_ups_11", "UPS Standard", 1),
        _rate("parcelone_ups_07", "UPS Express", 1),
        _rate("parcelone_ups_65", "UPS Express Saver", 1),
    ],
    [],
]
