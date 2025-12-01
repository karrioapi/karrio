import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.dhl_poland import units
from .fixture import gateway


class TestDHLPolandRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestDHLPolandServiceFiltering(unittest.TestCase):
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
        self.assertIn("dhl_poland_premium", service_codes)
        self.assertIn("dhl_poland_connect", service_codes)
        self.assertIn("dhl_poland_international", service_codes)

    def test_domestic_services_marked_correctly(self):
        """Test that domestic services have domicile=True."""
        domestic_services = [
            s for s in self.services if s.service_code == "dhl_poland_premium"
        ]

        self.assertEqual(len(domestic_services), 1)
        self.assertTrue(
            domestic_services[0].domicile, "Domestic service should have domicile=True"
        )
        self.assertIsNone(
            domestic_services[0].international,
            "Domestic service should not have international flag set",
        )

    def test_international_services_marked_correctly(self):
        """Test that international services have international=True."""
        international_services = [
            s for s in self.services if s.service_code == "dhl_poland_international"
        ]

        self.assertEqual(len(international_services), 1)
        self.assertTrue(
            international_services[0].international,
            "International service should have international=True",
        )
        self.assertIsNone(
            international_services[0].domicile,
            "International service should not have domicile flag set",
        )

    def test_domestic_request_returns_only_domestic_services(self):
        """Test that domestic request only returns domestic services."""
        # Simulate domestic request (PL to PL)
        domestic_request = RateRequest(
            **{
                "shipper": {"postal_code": "00909", "country_code": "PL"},
                "recipient": {"postal_code": "00001", "country_code": "PL"},
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

        # All returned services should be domestic
        service_codes = [rate.service for rate in rates]
        self.assertIn("dhl_poland_premium", service_codes)
        self.assertNotIn(
            "dhl_poland_international",
            service_codes,
            "International services should not be returned for domestic requests",
        )

    def test_international_request_returns_only_international_services(self):
        """Test that international request only returns international services."""
        # Simulate international request (PL to DE)
        international_request = RateRequest(
            **{
                "shipper": {"postal_code": "00909", "country_code": "PL"},
                "recipient": {"postal_code": "10115", "country_code": "DE"},
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
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
        self.assertIn("dhl_poland_international", service_codes)
        self.assertNotIn(
            "dhl_poland_premium",
            service_codes,
            "Domestic services should not be returned for international requests",
        )


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {"postal_code": "00909", "country_code": "PL"},
    "recipient": {"postal_code": "00001", "country_code": "PL"},
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
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "DHL Poland Premium",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "dhl_poland_premium",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "DHL Poland Polska",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "dhl_poland_polska",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "DHL Poland 09",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "dhl_poland_09",
            "total_charge": 0.0,
        },
        {
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "DHL Poland 12",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "dhl_poland_12",
            "total_charge": 0.0,
        },
    ],
    [],
]
