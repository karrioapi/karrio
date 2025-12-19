import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.gls_group import units
from .fixture import gateway


class TestGLSGroupRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestGLSGroupServiceFiltering(unittest.TestCase):
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
        self.assertIn("gls_parcel", service_codes)
        self.assertIn("gls_express", service_codes)
        self.assertIn("gls_euro_business_parcel", service_codes)

    def test_domestic_service_marked_correctly(self):
        """Test that domestic service has domicile=True."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "gls_parcel"), None
        )

        self.assertIsNotNone(domestic_service)
        self.assertTrue(
            domestic_service.domicile, "Domestic service should have domicile=True"
        )
        self.assertIsNone(
            domestic_service.international,
            "Domestic service should not have international flag set",
        )

    def test_international_service_marked_correctly(self):
        """Test that international service has international=True and domicile=False."""
        international_service = next(
            (s for s in self.services if s.service_code == "gls_euro_business_parcel"),
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
                    "postal_code": "12345",
                    "city": "Berlin",
                    "country_code": "DE",
                },
                "recipient": {
                    "postal_code": "54321",
                    "city": "Munich",
                    "country_code": "DE",
                },
                "parcels": [
                    {
                        "weight": 5.0,
                        "weight_unit": "KG",
                        "length": 20.0,
                        "width": 15.0,
                        "height": 10.0,
                        "dimension_unit": "CM",
                    }
                ],
            }
        )

        parsed_response = karrio.Rating.fetch(domestic_request).from_(gateway).parse()
        rates = parsed_response[0]

        # All returned services should be domestic
        service_codes = [rate.service for rate in rates]
        self.assertIn("gls_parcel", service_codes)
        self.assertNotIn(
            "gls_euro_business_parcel",
            service_codes,
            "International services should not be returned for domestic requests",
        )

    def test_international_request_returns_only_international_services(self):
        """Test that international request only returns international services."""
        # Simulate international request (DE to FR)
        international_request = RateRequest(
            **{
                "shipper": {
                    "postal_code": "12345",
                    "city": "Berlin",
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
                        "length": 20.0,
                        "width": 15.0,
                        "height": 10.0,
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
        self.assertIn("gls_euro_business_parcel", service_codes)
        self.assertNotIn(
            "gls_parcel",
            service_codes,
            "Domestic services should not be returned for international requests",
        )

    def test_weight_limits_respected(self):
        """Test that weight limits are properly checked."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "gls_parcel"), None
        )

        self.assertIsNotNone(domestic_service)
        self.assertEqual(domestic_service.min_weight, 0.01)
        self.assertEqual(domestic_service.max_weight, 31.5)
        self.assertEqual(domestic_service.weight_unit, "KG")


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "recipient": {
        "address_line1": "Market Street",
        "address_line2": "456",
        "city": "Munich",
        "country_code": "DE",
        "email": "recipient@example.com",
        "person_name": "Jane Smith",
        "postal_code": "54321",
        "phone_number": "+49891234567",
    },
    "shipper": {
        "address_line1": "Main Street",
        "address_line2": "123",
        "city": "Berlin",
        "country_code": "DE",
        "email": "shipper@example.com",
        "person_name": "John Doe",
        "phone_number": "+49301234567",
        "postal_code": "12345",
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
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "GLS Parcel",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "gls_parcel",
            "total_charge": 0.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "GLS Express",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "gls_express",
            "total_charge": 0.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "GLS Guaranteed24",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "gls_guaranteed24",
            "total_charge": 0.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "gls_group",
            "carrier_name": "gls_group",
            "currency": "EUR",
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "GLS Business Parcel",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "gls_business_parcel",
            "total_charge": 0.0,
            "transit_days": 2,
        },
    ],
    [],
]
