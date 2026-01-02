import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.hermes import units
from .fixture import gateway


class TestHermesRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestHermesServiceFiltering(unittest.TestCase):
    """Test service filtering for domestic vs international shipments."""

    maxDiff = None

    def setUp(self):
        """Load default services."""
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        """Test that default services are loaded."""
        self.assertGreater(len(self.services), 0, "Services should be loaded")

        # Check that we have both domestic and international services
        service_codes = [s.service_code for s in self.services]
        self.assertIn("hermes_standard", service_codes)
        self.assertIn("hermes_international", service_codes)

    def test_domestic_service_marked_correctly(self):
        """Test that domestic service has domicile=True."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "hermes_standard"), None
        )

        self.assertIsNotNone(domestic_service)
        self.assertTrue(
            domestic_service.domicile, "Domestic service should have domicile=True"
        )

    def test_international_service_marked_correctly(self):
        """Test that international service has international=True and domicile=False."""
        international_service = next(
            (s for s in self.services if s.service_code == "hermes_international"),
            None,
        )

        self.assertIsNotNone(international_service)
        self.assertTrue(
            international_service.international,
            "International service should have international=True",
        )
        self.assertFalse(
            international_service.domicile,
            "International service should have domicile=False",
        )

    def test_domestic_request_returns_only_domestic_services(self):
        """Test that domestic request only returns domestic services."""
        # Simulate domestic request (DE to DE)
        domestic_request = RateRequest(
            **{
                "shipper": {
                    "postal_code": "22419",
                    "city": "Hamburg",
                    "country_code": "DE",
                },
                "recipient": {
                    "postal_code": "10115",
                    "city": "Berlin",
                    "country_code": "DE",
                },
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
                        "length": 30.0,
                        "width": 20.0,
                        "height": 15.0,
                        "dimension_unit": "CM",
                    }
                ],
            }
        )

        parsed_response = karrio.Rating.fetch(domestic_request).from_(gateway).parse()
        rates = parsed_response[0]

        # All returned services should be domestic
        service_codes = [rate.service for rate in rates]
        self.assertIn("hermes_standard", service_codes)
        self.assertNotIn(
            "hermes_international",
            service_codes,
            "International services should not be returned for domestic requests",
        )

    def test_international_request_returns_only_international_services(self):
        """Test that international request only returns international services."""
        # Simulate international request (DE to FR)
        international_request = RateRequest(
            **{
                "shipper": {
                    "postal_code": "22419",
                    "city": "Hamburg",
                    "country_code": "DE",
                },
                "recipient": {
                    "postal_code": "75001",
                    "city": "Paris",
                    "country_code": "FR",
                },
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
                        "length": 30.0,
                        "width": 20.0,
                        "height": 15.0,
                        "dimension_unit": "CM",
                    }
                ],
            }
        )

        parsed_response = (
            karrio.Rating.fetch(international_request).from_(gateway).parse()
        )
        rates = parsed_response[0]

        # All returned services should be international
        service_codes = [rate.service for rate in rates]
        self.assertIn("hermes_international", service_codes)
        self.assertNotIn(
            "hermes_standard",
            service_codes,
            "Domestic services should not be returned for international requests",
        )

    def test_weight_limits_respected(self):
        """Test that weight limits are properly set."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "hermes_standard"), None
        )

        self.assertIsNotNone(domestic_service)
        self.assertEqual(domestic_service.min_weight, 0.01)
        self.assertEqual(domestic_service.max_weight, 31.5)
        self.assertEqual(domestic_service.weight_unit, "KG")


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "recipient": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "country_code": "DE",
        "person_name": "Max Mustermann",
        "postal_code": "22419",
        "phone_number": "+49401234567",
    },
    "shipper": {
        "address_line1": "Essener Bogen 1",
        "city": "Hamburg",
        "country_code": "DE",
        "person_name": "Test Company",
        "postal_code": "22419",
        "phone_number": "+49401234567",
    },
    "parcels": [
        {
            "dimension_unit": "CM",
            "height": 15.0,
            "length": 30.0,
            "weight": 5,
            "weight_unit": "KG",
            "width": 20.0,
        }
    ],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "Hermes Standard",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "hermes_standard",
            "total_charge": 0.0,
            "transit_days": 2,
        },
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "Hermes Next Day",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "hermes_next_day",
            "total_charge": 0.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "Hermes Stated Day",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "hermes_stated_day",
            "total_charge": 0.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "hermes",
            "carrier_name": "hermes",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "Hermes Parcel Shop",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "hermes_parcel_shop",
            "total_charge": 0.0,
            "transit_days": 2,
        },
    ],
    [],
]
