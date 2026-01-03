import unittest
import karrio.sdk as karrio
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.landmark import units
from .fixture import gateway


class TestLandmarkRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_request_data)

    def test_parse_rate_response(self):
        parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

        self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


class TestLandmarkServiceConfiguration(unittest.TestCase):
    """Test that Landmark services are properly configured."""

    maxDiff = None

    def setUp(self):
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        """Test that default services are loaded from CSV."""
        self.assertGreater(len(self.services), 0, "Services should be loaded")

        service_codes = [s.service_code for s in self.services]
        self.assertIn("landmark_maxipak_scan_ddp", service_codes)
        self.assertIn("landmark_maxipak_scan_ddu", service_codes)
        self.assertIn("landmark_minipak_scan_ddp", service_codes)
        self.assertIn("landmark_minipak_scan_ddu", service_codes)

    def test_maxipak_ddp_service_structure(self):
        """Test MaxiPak DDP service has correct structure."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "landmark_maxipak_scan_ddp"),
            None,
        )

        self.assertIsNotNone(maxipak_ddp)
        self.assertEqual(maxipak_ddp.currency, "GBP")
        self.assertGreater(len(maxipak_ddp.zones), 0)
        # Weight limits at service level
        self.assertEqual(maxipak_ddp.min_weight, 0)
        self.assertEqual(maxipak_ddp.max_weight, 30)

    def test_minipak_ddp_service_structure(self):
        """Test MiniPak DDP service has correct structure."""
        minipak_ddp = next(
            (s for s in self.services if s.service_code == "landmark_minipak_scan_ddp"),
            None,
        )

        self.assertIsNotNone(minipak_ddp)
        self.assertEqual(minipak_ddp.currency, "GBP")

        all_countries = {
            code
            for zone in minipak_ddp.zones
            if zone.country_codes
            for code in zone.country_codes
        }
        # MiniPak DDP is available for all zones including US, CA, AU
        self.assertIn("US", all_countries, "MiniPak DDP should include US")
        self.assertIn("DE", all_countries, "MiniPak DDP should include EU countries")

        # Weight limits at service level
        self.assertLessEqual(minipak_ddp.max_weight, 2.0, "MiniPak max weight should be 2kg")

    def test_all_services_have_zones_and_rates(self):
        """Test that all services have zones with valid rates."""
        for service in self.services:
            self.assertGreater(
                len(service.zones),
                0,
                f"Service {service.service_code} should have zones",
            )

            for zone in service.zones:
                self.assertIsNotNone(
                    zone.rate,
                    f"Zone {zone.label} in {service.service_code} should have rate",
                )
                self.assertGreater(
                    zone.rate,
                    0,
                    f"Zone {zone.label} in {service.service_code} should have positive rate",
                )


class TestLandmarkZoneConfiguration(unittest.TestCase):
    """Test zone-based pricing configuration."""

    maxDiff = None

    def setUp(self):
        self.maxipak_ddp = next(
            (
                s
                for s in units.DEFAULT_SERVICES
                if s.service_code == "landmark_maxipak_scan_ddp"
            ),
            None,
        )

    def test_us_zone_exists(self):
        """Test that US zone exists."""
        us_zones = [
            z
            for z in self.maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes
        ]

        self.assertGreater(len(us_zones), 0, "US zone should exist")

    def test_eu_zone_coverage(self):
        """Test that EU zones cover expected countries."""
        eu_countries = {
            code
            for zone in self.maxipak_ddp.zones
            if zone.label and "EU Zone" in zone.label and zone.country_codes
            for code in zone.country_codes
        }

        expected_countries = {"DE", "FR", "BE", "NL", "ES", "IT", "PL"}
        self.assertTrue(
            expected_countries.issubset(eu_countries),
            f"EU zones should cover key countries. Missing: {expected_countries - eu_countries}",
        )

    def test_germany_rate_lower_than_us(self):
        """Test that Germany rates are lower than US rates."""
        de_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes and "DE" in z.country_codes
            ),
            None,
        )

        us_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes and "US" in z.country_codes
            ),
            None,
        )

        self.assertIsNotNone(de_zone)
        self.assertIsNotNone(us_zone)
        self.assertLess(de_zone.rate, us_zone.rate, "Germany should be cheaper than US")

    def test_transit_times_defined(self):
        """Test that transit times are defined for zones."""
        zones_with_transit = [z for z in self.maxipak_ddp.zones if z.transit_days]

        self.assertGreater(
            len(zones_with_transit), 0, "Zones should have transit times"
        )

        us_zones = [
            z
            for z in self.maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes
        ]
        if us_zones:
            self.assertEqual(us_zones[0].transit_days, 7, "US transit should be 7 days")


class TestLandmarkRateScenarios(unittest.TestCase):
    """Test realistic shipping scenarios."""

    maxDiff = None

    def setUp(self):
        self.maxipak_ddp = next(
            (
                s
                for s in units.DEFAULT_SERVICES
                if s.service_code == "landmark_maxipak_scan_ddp"
            ),
            None,
        )

    def test_service_weight_limits(self):
        """Test that service has weight limits defined."""
        self.assertIsNotNone(self.maxipak_ddp.min_weight, "Service should have min_weight")
        self.assertIsNotNone(self.maxipak_ddp.max_weight, "Service should have max_weight")
        self.assertEqual(self.maxipak_ddp.min_weight, 0, "Min weight should be 0")
        self.assertEqual(self.maxipak_ddp.max_weight, 30, "Max weight should be 30kg")

    def test_us_zone_rate(self):
        """Test that US zone has expected rate."""
        us_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes and "US" in z.country_codes
            ),
            None,
        )

        self.assertIsNotNone(us_zone, "Should find US zone")
        self.assertEqual(us_zone.rate, 5.71, "US rate should be £5.71")

    def test_eu_zone1_rate(self):
        """Test that EU Zone 1 has expected rate."""
        eu_zone1 = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.label == "EU Zone 1"
            ),
            None,
        )

        self.assertIsNotNone(eu_zone1, "Should find EU Zone 1")
        self.assertEqual(eu_zone1.rate, 4.33, "EU Zone 1 rate should be £4.33")


if __name__ == "__main__":
    unittest.main()


rate_request_data = {
    "shipper": {
        "postal_code": "SW1A 1AA",
        "city": "London",
        "country_code": "GB",
        "address_line1": "123 Test Street",
    },
    "recipient": {
        "postal_code": "10001",
        "city": "New York",
        "country_code": "US",
        "state_code": "NY",
        "address_line1": "456 Main Street",
    },
    "parcels": [
        {
            "weight": 0.5,
            "weight_unit": "KG",
            "length": 20.0,
            "width": 15.0,
            "height": 10.0,
            "dimension_unit": "CM",
        }
    ],
}


ParsedRateResponse = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 5.71,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MaxiPak Scan DDP",
                "shipping_charges": 5.71,
                "shipping_currency": "GBP",
            },
            "service": "landmark_maxipak_scan_ddp",
            "total_charge": 5.71,
            "transit_days": 7,
        },
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 5.71,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MaxiPak Scan DDU",
                "shipping_charges": 5.71,
                "shipping_currency": "GBP",
            },
            "service": "landmark_maxipak_scan_ddu",
            "total_charge": 5.71,
            "transit_days": 7,
        },
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 5.71,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MiniPak Scan DDP",
                "shipping_charges": 5.71,
                "shipping_currency": "GBP",
            },
            "service": "landmark_minipak_scan_ddp",
            "total_charge": 5.71,
            "transit_days": 7,
        },
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 5.71,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MiniPak Scan DDU",
                "shipping_charges": 5.71,
                "shipping_currency": "GBP",
            },
            "service": "landmark_minipak_scan_ddu",
            "total_charge": 5.71,
            "transit_days": 7,
        },
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 3.75,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MaxiPak Scan Postal DDP",
                "shipping_charges": 3.75,
                "shipping_currency": "GBP",
            },
            "service": "landmark_maxipak_scan_pddp",
            "total_charge": 3.75,
            "transit_days": 12,
        },
    ],
    [],
]
