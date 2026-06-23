"""Asendia carrier rate tests."""

import unittest

import karrio.lib as lib
import karrio.sdk as karrio
from karrio.core.models import RateRequest
from karrio.providers.asendia import units

from .fixture import gateway


class TestAsendiaRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


class TestAsendiaServiceFiltering(unittest.TestCase):
    """Test service filtering for domestic vs international shipments."""

    maxDiff = None

    def setUp(self):
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        self.assertGreater(len(self.services), 0, "Services should be loaded")

        service_codes = [s.service_code for s in self.services]
        self.assertIn("asendia_epaq_standard", service_codes)
        self.assertIn("asendia_epaq_returns_domestic", service_codes)
        self.assertIn("asendia_epaq_returns_international", service_codes)

    def test_domestic_service_marked_correctly(self):
        domestic_services = [s for s in self.services if s.service_code == "asendia_epaq_returns_domestic"]

        self.assertEqual(len(domestic_services), 1)
        self.assertTrue(domestic_services[0].domicile, "Domestic service should have domicile=True")

    def test_international_services_marked_correctly(self):
        international_services = [s for s in self.services if s.service_code == "asendia_epaq_standard"]

        self.assertEqual(len(international_services), 1)
        self.assertTrue(
            international_services[0].international,
            "International service should have international=True",
        )
        self.assertFalse(
            international_services[0].domicile,
            "International service should not have domicile=True",
        )

    def test_domestic_request_returns_only_domestic_services(self):
        domestic_request = RateRequest(
            **{
                "shipper": {"postal_code": "10115", "country_code": "DE"},
                "recipient": {"postal_code": "20095", "country_code": "DE"},
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
                    }
                ],
            }
        )

        parsed_response = karrio.Rating.fetch(domestic_request).from_(gateway).parse()
        rates = parsed_response[0]

        service_codes = [rate.service for rate in rates]
        self.assertIn("asendia_epaq_returns_domestic", service_codes)
        self.assertNotIn(
            "asendia_epaq_standard",
            service_codes,
            "International services should not be returned for domestic requests",
        )

    def test_international_request_returns_only_international_services(self):
        international_request = RateRequest(
            **{
                "shipper": {"postal_code": "10115", "country_code": "DE"},
                "recipient": {"postal_code": "SW1A 1AA", "country_code": "GB"},
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
                    }
                ],
            }
        )

        parsed_response = karrio.Rating.fetch(international_request).from_(gateway).parse()
        rates = parsed_response[0]

        service_codes = [rate.service for rate in rates]
        self.assertIn("asendia_epaq_standard", service_codes)
        self.assertNotIn(
            "asendia_epaq_returns_domestic",
            service_codes,
            "Domestic services should not be returned for international requests",
        )

    def test_weight_limits_respected(self):
        epaq_standard = next((s for s in self.services if s.service_code == "asendia_epaq_standard"), None)

        self.assertIsNotNone(epaq_standard, "EPAQSTD service should be loaded")
        self.assertEqual(epaq_standard.min_weight, 0.01)
        self.assertEqual(epaq_standard.max_weight, 31.5)
        self.assertEqual(epaq_standard.weight_unit, "KG")


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {"postal_code": "10115", "country_code": "DE"},
    "recipient": {"postal_code": "SW1A 1AA", "country_code": "GB"},
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "services": [],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ Standard",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_standard",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ Plus",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_plus",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ Select",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_select",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ Elite",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_elite",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ GO",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_go",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "asendia",
            "carrier_name": "asendia",
            "currency": "EUR",
            "extra_charges": [{"amount": 0.0, "currency": "EUR", "name": "Base Charge"}],
            "meta": {
                "service_name": "e-PAQ International Returns",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "asendia_epaq_returns_international",
            "total_charge": 0.0,
        },
    ],
    [],
]
