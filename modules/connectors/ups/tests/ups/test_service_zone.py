"""Tests for UPS ServiceZone alias resolution.

Verifies that ServiceZone.find() returns canonical (base) service names
regardless of origin zone, so that rate selection can match "ups_standard"
against rates returned from any origin (US, EU, CA, MX, PL).
"""

import unittest

from karrio.providers.ups import units as provider_units

ServiceZone = provider_units.ServiceZone
_ZONE_ALIAS_TO_BASE = provider_units._ZONE_ALIAS_TO_BASE


class TestServiceZoneFind(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    # ── EU origin ────────────────────────────────────────────────────

    def test_standard_eu_resolves_to_base(self):
        """ups_standard_eu (code 11, EU) → ups_standard."""
        result = ServiceZone.find("11", "EU")
        self.assertEqual(result.name_or_key, "ups_standard")

    def test_express_eu_resolves_to_base(self):
        """ups_express_eu (code 07, EU) → ups_express."""
        result = ServiceZone.find("07", "EU")
        self.assertEqual(result.name_or_key, "ups_express")

    def test_worldwide_saver_eu_resolves_to_base(self):
        """ups_worldwide_saver_eu (code 65, EU) → ups_worldwide_saver."""
        result = ServiceZone.find("65", "EU")
        self.assertEqual(result.name_or_key, "ups_worldwide_saver")

    def test_worldwide_express_plus_eu_resolves_to_base(self):
        """ups_worldwide_express_plus_eu (code 54, EU) → ups_worldwide_express_plus."""
        result = ServiceZone.find("54", "EU")
        self.assertEqual(result.name_or_key, "ups_worldwide_express_plus")

    def test_access_point_economy_eu_resolves_to_base(self):
        """ups_access_point_economy_eu (code 70, EU) → ups_access_point_economy."""
        result = ServiceZone.find("70", "EU")
        self.assertEqual(result.name_or_key, "ups_access_point_economy")

    # ── US origin (base services, no aliasing) ───────────────────────

    def test_standard_us_stays_base(self):
        """ups_standard (code 11, US) → ups_standard (no change)."""
        result = ServiceZone.find("11", "US")
        self.assertEqual(result.name_or_key, "ups_standard")

    def test_express_us_stays_base(self):
        """ups_express (code 07, US) → ups_express (no change)."""
        result = ServiceZone.find("07", "US")
        self.assertEqual(result.name_or_key, "ups_express")

    # ── CA origin ────────────────────────────────────────────────────

    def test_standard_ca_resolves_to_base(self):
        """ups_standard_ca (code 11, CA) → ups_standard."""
        result = ServiceZone.find("11", "CA")
        self.assertEqual(result.name_or_key, "ups_standard")

    def test_express_ca_resolves_to_base(self):
        """ups_express_ca (code 01, CA) → ups_next_day_air."""
        result = ServiceZone.find("01", "CA")
        self.assertEqual(result.name_or_key, "ups_next_day_air")

    def test_expedited_ca_resolves_to_base(self):
        """ups_expedited_ca (code 02, CA) → ups_2nd_day_air."""
        result = ServiceZone.find("02", "CA")
        self.assertEqual(result.name_or_key, "ups_2nd_day_air")

    # ── MX origin ────────────────────────────────────────────────────

    def test_standard_mx_resolves_to_base(self):
        """ups_standard_mx (code 11, MX) → ups_standard."""
        result = ServiceZone.find("11", "MX")
        self.assertEqual(result.name_or_key, "ups_standard")

    # ── PL origin ────────────────────────────────────────────────────

    def test_standard_pl_resolves_to_base(self):
        """ups_standard_pl (code 11, PL) → ups_standard."""
        result = ServiceZone.find("11", "PL")
        self.assertEqual(result.name_or_key, "ups_standard")

    def test_pl_unique_service_preserved(self):
        """ups_today_dedicated_courrier_pl (code 83, PL) has no base alias."""
        result = ServiceZone.find("83", "PL")
        self.assertEqual(result.name_or_key, "ups_today_dedicated_courrier_pl")

    # ── Unknown origin falls back to ServiceCode ─────────────────────

    def test_unknown_origin_falls_back(self):
        """Code 11 with unknown origin falls back to ServiceCode.map."""
        result = ServiceZone.find("11", "XX")
        self.assertEqual(result.name_or_key, "ups_standard")

    # ── Alias map integrity ──────────────────────────────────────────

    def test_alias_map_contains_eu_entries(self):
        """EU zone aliases are in the mapping."""
        self.assertEqual(_ZONE_ALIAS_TO_BASE["ups_standard_eu"], "ups_standard")
        self.assertEqual(_ZONE_ALIAS_TO_BASE["ups_express_eu"], "ups_express")

    def test_alias_map_does_not_contain_base_services(self):
        """Base services (first-defined) should not be in the alias map."""
        self.assertNotIn("ups_standard", _ZONE_ALIAS_TO_BASE)
        self.assertNotIn("ups_express", _ZONE_ALIAS_TO_BASE)
        self.assertNotIn("ups_ground", _ZONE_ALIAS_TO_BASE)

    def test_alias_map_contains_ca_entries(self):
        """CA zone aliases are in the mapping."""
        self.assertEqual(_ZONE_ALIAS_TO_BASE["ups_standard_ca"], "ups_standard")
        self.assertEqual(_ZONE_ALIAS_TO_BASE["ups_express_ca"], "ups_next_day_air")
        self.assertEqual(_ZONE_ALIAS_TO_BASE["ups_expedited_ca"], "ups_2nd_day_air")


if __name__ == "__main__":
    unittest.main()
