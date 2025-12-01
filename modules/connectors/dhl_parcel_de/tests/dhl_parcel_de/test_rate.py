import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.dhl_parcel_de import units
from .fixture import gateway


class TestDHLParcelDERating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestDHLParcelDEServiceFiltering(unittest.TestCase):
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
        self.assertIn("dhl_parcel_de_paket", service_codes)
        self.assertIn("dhl_parcel_de_europaket", service_codes)

    def test_domestic_service_marked_correctly(self):
        """Test that domestic service has domicile=True."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "dhl_parcel_de_paket"), None
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
            (s for s in self.services if s.service_code == "dhl_parcel_de_europaket"),
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
                    "postal_code": "53113",
                    "city": "Bonn",
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
        self.assertIn("dhl_parcel_de_paket", service_codes)
        self.assertNotIn(
            "dhl_parcel_de_europaket",
            service_codes,
            "International services should not be returned for domestic requests",
        )

    def test_international_request_returns_only_international_services(self):
        """Test that international request only returns international services."""
        # Simulate international request (DE to FR)
        international_request = RateRequest(
            **{
                "shipper": {
                    "postal_code": "53113",
                    "city": "Bonn",
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
        self.assertIn("dhl_parcel_de_europaket", service_codes)
        self.assertNotIn(
            "dhl_parcel_de_paket",
            service_codes,
            "Domestic services should not be returned for international requests",
        )

    def test_weight_limits_respected(self):
        """Test that weight limits are properly checked."""
        domestic_service = next(
            (s for s in self.services if s.service_code == "dhl_parcel_de_paket"), None
        )

        self.assertIsNotNone(domestic_service)
        self.assertEqual(domestic_service.min_weight, 0.01)
        self.assertEqual(domestic_service.max_weight, 31.5)
        self.assertEqual(domestic_service.weight_unit, "KG")


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
            "extra_charges": [
                {
                    "amount": 0.0,
                    "currency": "EUR",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "DHL Paket",
                "shipping_charges": 0.0,
                "shipping_currency": "EUR",
            },
            "service": "dhl_parcel_de_paket",
            "total_charge": 0.0,
        }
    ],
    [],
]
