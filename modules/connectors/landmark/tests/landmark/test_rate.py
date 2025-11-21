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
        self.assertGreater(len(maxipak_ddp.zones), 10)

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
        self.assertNotIn("US", all_countries, "MiniPak DDP should be EU only")
        self.assertNotIn("CA", all_countries, "MiniPak DDP should be EU only")
        self.assertNotIn("AU", all_countries, "MiniPak DDP should be EU only")

        max_weights = [z.max_weight for z in minipak_ddp.zones if z.max_weight]
        max_weight = max(max_weights) if max_weights else 0
        self.assertLessEqual(max_weight, 2.0, "MiniPak max weight should be 2kg")

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

    def test_us_zone_has_multiple_weight_tiers(self):
        """Test that US zone has multiple weight tiers."""
        us_zones = [
            z
            for z in self.maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes
        ]

        self.assertGreater(len(us_zones), 5, "US should have multiple weight tiers")

        weight_ranges = {(z.min_weight, z.max_weight) for z in us_zones}
        self.assertEqual(
            len(weight_ranges),
            len(us_zones),
            "Weight ranges should be unique",
        )

    def test_us_rates_increase_with_weight(self):
        """Test that US rates increase with weight."""
        us_zones = sorted(
            [
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.label == "United States"
                and z.max_weight
            ],
            key=lambda z: z.max_weight,
        )

        for i in range(len(us_zones) - 1):
            current_rate = us_zones[i].rate
            next_rate = us_zones[i + 1].rate
            self.assertLessEqual(
                current_rate,
                next_rate * 1.1,
                f"Rate should increase with weight: {us_zones[i].min_weight}-{us_zones[i].max_weight}kg @ £{current_rate} vs {us_zones[i+1].min_weight}-{us_zones[i+1].max_weight}kg @ £{next_rate}",
            )

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
        """Test that Germany rates are lower than US rates for same weight."""
        de_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "DE" in z.country_codes
                and z.min_weight == 0.5
                and z.max_weight == 1.0
            ),
            None,
        )

        us_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.min_weight == 0.5
                and z.max_weight == 1.0
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

    def test_zone_weight_ranges_no_gaps(self):
        """Test that weight ranges don't have gaps for each destination."""
        zones_by_destination = {}
        for zone in self.maxipak_ddp.zones:
            zones_by_destination.setdefault(zone.label, []).append(zone)

        for destination, zones in zones_by_destination.items():
            sorted_zones = sorted(
                [z for z in zones if z.min_weight is not None],
                key=lambda z: z.min_weight,
            )

            if len(sorted_zones) < 2:
                continue

            for i in range(len(sorted_zones) - 1):
                current_max = sorted_zones[i].max_weight
                next_min = sorted_zones[i + 1].min_weight

                self.assertEqual(
                    current_max,
                    next_min,
                    f"{destination}: Gap in weight ranges - zone {i} ends at {current_max}kg, zone {i+1} starts at {next_min}kg",
                )


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

    def test_light_package_to_us_rate(self):
        """Test rate for 0.3kg package to US."""
        matching_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.min_weight is not None
                and z.max_weight is not None
                and z.min_weight <= 0.3 < z.max_weight
            ),
            None,
        )

        self.assertIsNotNone(matching_zone, "Should find zone for 0.3kg to US")
        self.assertEqual(matching_zone.rate, 6.86, "0.3kg to US should cost £6.86")

    def test_medium_package_to_us_rate(self):
        """Test rate for 0.75kg package to US."""
        matching_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.min_weight is not None
                and z.max_weight is not None
                and z.min_weight <= 0.75 < z.max_weight
            ),
            None,
        )

        self.assertIsNotNone(matching_zone, "Should find zone for 0.75kg to US")
        self.assertEqual(matching_zone.rate, 8.78, "0.75kg to US should cost £8.78")

    def test_heavy_package_to_us_rate(self):
        """Test rate for 1.5kg package to US."""
        matching_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.min_weight is not None
                and z.max_weight is not None
                and z.min_weight <= 1.5 < z.max_weight
            ),
            None,
        )

        self.assertIsNotNone(matching_zone, "Should find zone for 1.5kg to US")
        self.assertEqual(matching_zone.rate, 10.81, "1.5kg to US should cost £10.81")

    def test_package_on_tier_boundary(self):
        """Test package weight exactly on tier boundary."""
        matching_zone = next(
            (
                z
                for z in self.maxipak_ddp.zones
                if z.country_codes
                and "US" in z.country_codes
                and z.min_weight is not None
                and z.max_weight is not None
                and z.min_weight <= 0.5 < z.max_weight
            ),
            None,
        )

        if matching_zone:
            self.assertEqual(
                matching_zone.min_weight,
                0.5,
                "0.5kg should match tier starting at 0.5kg",
            )


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
                    "amount": 8.78,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MaxiPak Scan DDP",
            },
            "service": "landmark_maxipak_scan_ddp",
            "total_charge": 8.78,
            "transit_days": 7,
        },
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "currency": "GBP",
            "extra_charges": [
                {
                    "amount": 8.78,
                    "currency": "GBP",
                    "name": "Base Charge",
                }
            ],
            "meta": {
                "service_name": "MaxiPak Scan DDU",
            },
            "service": "landmark_maxipak_scan_ddu",
            "total_charge": 8.78,
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
            },
            "service": "landmark_maxipak_scan_pddp",
            "total_charge": 3.75,
            "transit_days": 12,
        },
    ],
    [],
]
