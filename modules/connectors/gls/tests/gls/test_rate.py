import unittest

import karrio.sdk as karrio
from karrio.core.models import RateRequest
from karrio.core.utils import DP
from karrio.providers.gls import units

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
        """Test that default services are loaded.

        GLS confirmed the wire product catalogue is just PARCEL and EXPRESS;
        the actual delivery network is selected from the recipient address,
        so a single ``gls_parcel`` service carries both domestic and EU
        cross-border zones in the service sheet.
        """
        self.assertGreater(len(self.services), 0, "Services should be loaded")
        service_codes = [s.service_code for s in self.services]
        self.assertIn("gls_parcel", service_codes)
        self.assertIn("gls_express", service_codes)

    def test_gls_parcel_covers_domestic_and_international(self):
        """gls_parcel exposes a domestic (DE, domicile=True) zone and an
        EU cross-border (international=True) zone — the single PARCEL
        product handling both."""
        parcel = next((s for s in self.services if s.service_code == "gls_parcel"), None)
        self.assertIsNotNone(parcel)
        self.assertTrue(parcel.domicile, "gls_parcel should carry a domestic zone")
        self.assertTrue(parcel.international, "gls_parcel should also carry an international zone")

    def test_domestic_request_returns_gls_parcel(self):
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

        service_codes = [rate.service for rate in rates]
        self.assertIn("gls_parcel", service_codes)

    def test_international_request_returns_gls_parcel(self):
        """DE → FR should still surface ``gls_parcel`` — the single
        PARCEL product covers EU cross-border via its international zone."""
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

        parsed_response = karrio.Rating.fetch(international_request).from_(gateway).parse()
        rates = parsed_response[0]

        service_codes = [rate.service for rate in rates]
        self.assertIn("gls_parcel", service_codes)

    def test_weight_limits_respected(self):
        """Test that weight limits are properly checked."""
        domestic_service = next((s for s in self.services if s.service_code == "gls_parcel"), None)

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
            "carrier_id": "gls",
            "carrier_name": "gls",
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
            "carrier_id": "gls",
            "carrier_name": "gls",
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
    ],
    [],
]
