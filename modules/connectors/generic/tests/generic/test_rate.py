import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.generic import units
from .fixture import gateway


class TestGenericRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestGenericServiceConfiguration(unittest.TestCase):
    """Test that generic carrier services work with rating proxy."""

    maxDiff = None

    def setUp(self):
        """Load default services."""
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        """Test that default services are loaded."""
        self.assertGreater(len(self.services), 0, "Services should be loaded")

        # Check that we have the standard service
        service_codes = [s.service_code for s in self.services]
        self.assertIn("standard_service", service_codes)

    def test_standard_service_configuration(self):
        """Test that standard service has correct configuration."""
        standard_service = next(
            (s for s in self.services if s.service_code == "standard_service"), None
        )

        self.assertIsNotNone(standard_service)
        self.assertEqual(standard_service.service_name, "Standard Service")
        self.assertEqual(standard_service.currency, "USD")
        self.assertIsNotNone(standard_service.zones)
        self.assertGreater(len(standard_service.zones), 0)

    def test_services_without_domicile_international_flags(self):
        """Test that services without domicile/international flags match all destinations."""
        standard_service = next(
            (s for s in self.services if s.service_code == "standard_service"), None
        )

        # Generic services don't specify domicile/international flags
        # They should default to None and match all destinations
        self.assertIsNone(
            standard_service.domicile,
            "Generic services should not have domicile flag set by default",
        )
        self.assertIsNone(
            standard_service.international,
            "Generic services should not have international flag set by default",
        )

    def test_domestic_request_returns_generic_service(self):
        """Test that domestic request returns generic services (no filtering)."""
        # Simulate domestic request
        domestic_request = RateRequest(
            **{
                "shipper": {"postal_code": "11111", "country_code": "US"},
                "recipient": {"postal_code": "22222", "country_code": "US"},
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "LB",
                    }
                ],
            }
        )

        parsed_response = karrio.Rating.fetch(domestic_request).from_(gateway).parse()
        rates = parsed_response[0]

        # Generic services should be returned (no filtering by default)
        service_codes = [rate.service for rate in rates]
        self.assertIn(
            "standard_service",
            service_codes,
            "Generic services should be returned for domestic requests",
        )

    def test_international_request_returns_generic_service(self):
        """Test that international request returns generic services (no filtering)."""
        # Simulate international request
        international_request = RateRequest(
            **{
                "shipper": {"postal_code": "11111", "country_code": "US"},
                "recipient": {"postal_code": "M5H 2N2", "country_code": "CA"},
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "LB",
                    }
                ],
            }
        )

        parsed_response = (
            karrio.Rating.fetch(international_request).from_(gateway).parse()
        )
        rates = parsed_response[0]

        # Generic services should be returned (no filtering by default)
        service_codes = [rate.service for rate in rates]
        self.assertIn(
            "standard_service",
            service_codes,
            "Generic services should be returned for international requests",
        )


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
            "extra_charges": [
                {
                    "amount": 100.0,
                    "currency": "USD",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "Standard Service",
                "shipping_charges": 100.0,
                "shipping_currency": "USD",
            },
            "service": "standard_service",
            "total_charge": 100.0,
        }
    ],
    [],
]
