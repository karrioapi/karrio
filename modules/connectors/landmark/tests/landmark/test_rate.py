"""Landmark Global rate tests."""

import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.providers.landmark import units


class TestLandmarkRates(unittest.TestCase):
    """Test Landmark rate calculations using default CSV sheet."""

    maxDiff = None

    def setUp(self):
        """Load default services from CSV."""
        self.services = units.DEFAULT_SERVICES

    def test_default_services_loaded(self):
        """Test that default services are loaded from CSV."""
        self.assertGreater(len(self.services), 0, "Services should be loaded from CSV")

        # Check that we have the expected services
        service_codes = [s.service_code for s in self.services]
        self.assertIn("LGINTSTD", service_codes)
        self.assertIn("LGINTSTDU", service_codes)
        self.assertIn("LGINTBPIP", service_codes)
        self.assertIn("LGINTBPIU", service_codes)

    def test_maxipak_ddp_service_structure(self):
        """Test MaxiPak DDP service has correct structure."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        self.assertIsNotNone(maxipak_ddp)
        self.assertEqual(maxipak_ddp.service_name, "MaxiPak Scan DDP")
        self.assertEqual(maxipak_ddp.currency, "GBP")

        # Should have multiple zones
        self.assertGreater(len(maxipak_ddp.zones), 10)

    def test_weight_tiers_for_us_zone(self):
        """Test that US zone has multiple weight tiers."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Filter US zones
        us_zones = [
            z
            for z in maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes
        ]

        # Should have multiple weight tiers for US
        self.assertGreater(len(us_zones), 5, "Should have multiple weight tiers for US")

        # Check that zones have different weight ranges
        weight_ranges = [(z.min_weight, z.max_weight) for z in us_zones]
        self.assertEqual(
            len(weight_ranges), len(set(weight_ranges)), "Weight ranges should be unique"
        )

    def test_zone_prices_increase_with_weight(self):
        """Test that prices generally increase with weight within same destination."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Get US zones sorted by max_weight
        us_zones = [
            z
            for z in maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes and z.label == "United States"
        ]
        us_zones_sorted = sorted(
            us_zones, key=lambda z: z.max_weight if z.max_weight else float("inf")
        )

        # Check that rates generally increase (allowing for some variation)
        for i in range(len(us_zones_sorted) - 1):
            current_rate = us_zones_sorted[i].rate
            next_rate = us_zones_sorted[i + 1].rate

            # Rate should increase or stay same as weight increases
            self.assertLessEqual(
                current_rate,
                next_rate * 1.1,  # Allow 10% tolerance for pricing variations
                f"Rate should increase with weight: {us_zones_sorted[i].min_weight}-{us_zones_sorted[i].max_weight}kg @ £{current_rate} vs {us_zones_sorted[i+1].min_weight}-{us_zones_sorted[i+1].max_weight}kg @ £{next_rate}",
            )

    def test_light_package_to_us_rate(self):
        """Test rate for 0.3kg package to US."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Find matching zone for 0.3kg to US
        matching_zone = None
        for zone in maxipak_ddp.zones:
            if zone.country_codes and "US" in zone.country_codes:
                if (
                    zone.min_weight is not None
                    and zone.max_weight is not None
                    and zone.min_weight <= 0.3 < zone.max_weight
                ):
                    matching_zone = zone
                    break

        self.assertIsNotNone(matching_zone, "Should find matching zone for 0.3kg to US")
        self.assertEqual(
            matching_zone.rate, 6.86, "0.3kg to US should cost £6.86 (0.25-0.5kg tier)"
        )

    def test_medium_package_to_us_rate(self):
        """Test rate for 0.75kg package to US."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Find matching zone for 0.75kg to US
        matching_zone = None
        for zone in maxipak_ddp.zones:
            if zone.country_codes and "US" in zone.country_codes:
                if (
                    zone.min_weight is not None
                    and zone.max_weight is not None
                    and zone.min_weight <= 0.75 < zone.max_weight
                ):
                    matching_zone = zone
                    break

        self.assertIsNotNone(
            matching_zone, "Should find matching zone for 0.75kg to US"
        )
        self.assertEqual(
            matching_zone.rate,
            8.78,
            "0.75kg to US should cost £8.78 (0.5-1.0kg tier)",
        )

    def test_heavy_package_to_us_rate(self):
        """Test rate for 1.5kg package to US."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Find matching zone for 1.5kg to US
        matching_zone = None
        for zone in maxipak_ddp.zones:
            if zone.country_codes and "US" in zone.country_codes:
                if (
                    zone.min_weight is not None
                    and zone.max_weight is not None
                    and zone.min_weight <= 1.5 < zone.max_weight
                ):
                    matching_zone = zone
                    break

        self.assertIsNotNone(
            matching_zone, "Should find matching zone for 1.5kg to US"
        )
        self.assertEqual(
            matching_zone.rate,
            10.81,
            "1.5kg to US should cost £10.81 (1.0-2.0kg tier)",
        )

    def test_eu_zone_coverage(self):
        """Test that EU zones cover expected countries."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Get all EU country codes
        eu_countries = set()
        for zone in maxipak_ddp.zones:
            if zone.label and "EU Zone" in zone.label:
                if zone.country_codes:
                    eu_countries.update(zone.country_codes)

        # Check key EU countries are covered
        expected_countries = {"DE", "FR", "BE", "NL", "ES", "IT", "PL"}
        self.assertTrue(
            expected_countries.issubset(eu_countries),
            f"EU zones should cover key countries. Missing: {expected_countries - eu_countries}",
        )

    def test_germany_rate_lower_than_us(self):
        """Test that Germany rates are lower than US rates (EU Zone 1 vs US)."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Get 1kg rate for Germany (EU Zone 1)
        de_zone = None
        for zone in maxipak_ddp.zones:
            if (
                zone.country_codes
                and "DE" in zone.country_codes
                and zone.min_weight == 0.5
                and zone.max_weight == 1.0
            ):
                de_zone = zone
                break

        # Get 1kg rate for US
        us_zone = None
        for zone in maxipak_ddp.zones:
            if (
                zone.country_codes
                and "US" in zone.country_codes
                and zone.min_weight == 0.5
                and zone.max_weight == 1.0
            ):
                us_zone = zone
                break

        self.assertIsNotNone(de_zone)
        self.assertIsNotNone(us_zone)
        self.assertLess(
            de_zone.rate,
            us_zone.rate,
            "Germany (EU Zone 1) should be cheaper than US for same weight",
        )

    def test_minipak_eu_only_restriction(self):
        """Test that MiniPak DDP is EU only."""
        minipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTBPIP"), None
        )

        self.assertIsNotNone(minipak_ddp)

        # Get all country codes covered by MiniPak DDP
        all_countries = set()
        for zone in minipak_ddp.zones:
            if zone.country_codes:
                all_countries.update(zone.country_codes)

        # Should NOT include US or other non-EU countries
        self.assertNotIn("US", all_countries, "MiniPak DDP should not cover US")
        self.assertNotIn("CA", all_countries, "MiniPak DDP should not cover Canada")
        self.assertNotIn("AU", all_countries, "MiniPak DDP should not cover Australia")

    def test_minipak_weight_limit(self):
        """Test that MiniPak services have 2kg weight limit."""
        minipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTBPIP"), None
        )

        # Check maximum weight across all zones
        max_weights = [z.max_weight for z in minipak_ddp.zones if z.max_weight]
        max_weight = max(max_weights) if max_weights else 0

        self.assertLessEqual(
            max_weight, 2.0, "MiniPak services should have max 2kg weight limit"
        )

    def test_transit_times_defined(self):
        """Test that transit times are defined for zones."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Check that zones have transit times
        zones_with_transit = [z for z in maxipak_ddp.zones if z.transit_days]

        self.assertGreater(
            len(zones_with_transit), 0, "Zones should have transit times defined"
        )

        # Check US transit time is 7 days
        us_zones = [
            z
            for z in maxipak_ddp.zones
            if z.country_codes and "US" in z.country_codes
        ]
        if us_zones:
            self.assertEqual(
                us_zones[0].transit_days, 7, "US transit time should be 7 days"
            )

    def test_zone_weight_ranges_no_gaps(self):
        """Test that weight ranges don't have gaps for each destination."""
        maxipak_ddp = next(
            (s for s in self.services if s.service_code == "LGINTSTD"), None
        )

        # Group zones by destination (using label for simplicity)
        zones_by_destination = {}
        for zone in maxipak_ddp.zones:
            if zone.label not in zones_by_destination:
                zones_by_destination[zone.label] = []
            zones_by_destination[zone.label].append(zone)

        # Check each destination
        for destination, zones in zones_by_destination.items():
            # Sort by min_weight
            sorted_zones = sorted(
                [z for z in zones if z.min_weight is not None],
                key=lambda z: z.min_weight,
            )

            if len(sorted_zones) < 2:
                continue

            # Check that each zone's max_weight equals next zone's min_weight
            for i in range(len(sorted_zones) - 1):
                current_max = sorted_zones[i].max_weight
                next_min = sorted_zones[i + 1].min_weight

                self.assertEqual(
                    current_max,
                    next_min,
                    f"{destination}: Gap in weight ranges - zone {i} ends at {current_max}kg, zone {i+1} starts at {next_min}kg",
                )

    def test_all_services_have_zones(self):
        """Test that all services have at least one zone defined."""
        for service in self.services:
            self.assertGreater(
                len(service.zones),
                0,
                f"Service {service.service_code} should have at least one zone",
            )

    def test_all_zones_have_rates(self):
        """Test that all zones have rates defined."""
        for service in self.services:
            for zone in service.zones:
                self.assertIsNotNone(
                    zone.rate,
                    f"Zone {zone.label} in service {service.service_code} should have a rate",
                )
                self.assertGreater(
                    zone.rate,
                    0,
                    f"Zone {zone.label} in service {service.service_code} should have positive rate",
                )


class TestLandmarkRateScenarios(unittest.TestCase):
    """Test realistic shipping scenarios with Landmark."""

    maxDiff = None

    def test_small_package_uk_to_us(self):
        """Test: Small package (0.5kg) from UK to US."""
        # This would normally use the full rating proxy
        # For now, we'll just verify the zone exists
        from karrio.providers.landmark import units

        maxipak_ddp = next(
            (s for s in units.DEFAULT_SERVICES if s.service_code == "LGINTSTD"), None
        )

        # Find zone for 0.5kg to US
        matching_zones = [
            z
            for z in maxipak_ddp.zones
            if z.country_codes
            and "US" in z.country_codes
            and z.min_weight is not None
            and z.max_weight is not None
            and z.min_weight <= 0.5 < z.max_weight
        ]

        self.assertEqual(len(matching_zones), 1, "Should find exactly one matching zone")
        self.assertEqual(matching_zones[0].rate, 8.78, "0.5kg to US should cost £8.78 (0.5-1.0kg tier)")

    def test_package_exactly_on_tier_boundary(self):
        """Test: Package weight exactly on tier boundary (0.5kg)."""
        from karrio.providers.landmark import units

        maxipak_ddp = next(
            (s for s in units.DEFAULT_SERVICES if s.service_code == "LGINTSTD"), None
        )

        # Weight = 0.5kg should match 0.5-1.0kg tier (inclusive min, exclusive max)
        matching_zones = [
            z
            for z in maxipak_ddp.zones
            if z.country_codes
            and "US" in z.country_codes
            and z.min_weight is not None
            and z.max_weight is not None
            and z.min_weight <= 0.5 < z.max_weight
        ]

        # With exclusive max, 0.5kg should match the 0.5-1.0kg tier
        if matching_zones:
            self.assertEqual(
                matching_zones[0].min_weight,
                0.5,
                "0.5kg should match tier starting at 0.5kg",
            )


if __name__ == "__main__":
    unittest.main()
