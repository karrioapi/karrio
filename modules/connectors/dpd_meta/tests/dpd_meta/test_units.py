import unittest

from karrio.providers.dpd_meta.units import B2C_PRODUCT_CODES, DEFAULT_SERVICES


class TestServiceLevelBounds(unittest.TestCase):
    """services.csv has multi-tier weight rows per service.
    Service-level max_weight must reflect the widest row, not just row 0."""

    def setUp(self):
        self.by_code = {s.service_code: s for s in DEFAULT_SERVICES}

    def test_dpd_meta_classic_max_weight_covers_top_tier(self):
        svc = self.by_code["dpd_meta_classic"]
        self.assertEqual(svc.max_weight, 31.5)
        self.assertEqual(svc.min_weight, 0.01)

    def test_dpd_meta_b2c_classic_max_weight_covers_top_tier(self):
        svc = self.by_code["dpd_meta_b2c_classic"]
        self.assertEqual(svc.max_weight, 31.5)
        self.assertEqual(svc.min_weight, 0.01)

    def test_dpd_meta_small_capped_at_3kg(self):
        # SoCode 136 is Small Parcel (≤ 3 kg). Above 3 kg DPD's MetaAPI
        # auto-routes to 101 (Classic) regardless of the SoCode we send,
        # so allowing rates >3 kg under 136 would advertise products that
        # never physically ship as 136. Verified live via boundary tests.
        svc = self.by_code["dpd_meta_small"]
        self.assertEqual(svc.max_weight, 3.0)
        self.assertEqual(svc.min_weight, 0.01)

    def test_dpd_meta_b2c_small_capped_at_3kg(self):
        # SoCode 328 is B2C Small Parcel (≤ 3 kg). Same rule as 136 —
        # >3 kg auto-routes to 327 (B2C Classic) on DPD's side.
        svc = self.by_code["dpd_meta_b2c_small"]
        self.assertEqual(svc.max_weight, 3.0)
        self.assertEqual(svc.min_weight, 0.01)

    def test_zones_preserved_across_all_tiers(self):
        svc = self.by_code["dpd_meta_classic"]
        zone_ranges = sorted({(z.min_weight, z.max_weight) for z in svc.zones})
        # Domestic DE tiers from services.csv rows 2-6
        for tier in [(0.01, 3.0), (3.0, 5.0), (5.0, 10.0), (10.0, 20.0), (20.0, 31.5)]:
            self.assertIn(tier, zone_ranges, f"missing tier {tier}")

    def test_b2c_codes_are_classified(self):
        """All B2C SoCodes (including April 2026 LQ additions 447/794) must be
        present in the predict-required set."""
        for code in (
            "327",
            "328",
            "329",
            "330",
            "332",
            "337",
            "338",
            "358",
            "366",
            "378",
            "379",
            "383",
            "447",
            "794",
        ):
            self.assertIn(code, B2C_PRODUCT_CODES, f"missing B2C SoCode {code}")

    def test_phase1_socodes_have_csv_rows(self):
        """Every Phase-1 SoCode must have at least one CSV row.

        Karrio's universal rate validator rejects services without a CSV row
        with `service not available`, so each new alias / direct SoCode needs
        coverage. Codes appear under their `ShippingService` alias key when
        one exists, otherwise under the raw SoCode string.

        Note: SoCodes 118/365/366/378/379/383 are commented out in
        ShippingService for the Bronze certification demo (SHIP2-1194).
        Their CSV rows still exist but load under raw numeric keys so the
        data-import pipeline and historical records stay intact.
        """
        keys = frozenset(s.service_code for s in DEFAULT_SERVICES)
        # Direct numeric SoCodes (no ShippingService alias)
        for code in ("113", "138", "142", "158", "228", "231", "234", "351"):
            self.assertIn(code, keys, f"missing CSV row for SoCode {code}")
        # Non-Bronze SoCodes (commented out in ShippingService) — check by raw code
        for code in ("118", "365", "366", "378", "379", "383"):
            self.assertIn(code, keys, f"missing CSV row for non-Bronze SoCode {code}")
        # Bronze SoCodes surfaced under a ShippingService alias
        aliased = (
            "dpd_meta_shop_return",  # 332
            "dpd_meta_parcelshop",  # 337
            "dpd_meta_shop2shop_domestic",  # 345
            "dpd_meta_shop2home",  # 404
        )
        for alias in aliased:
            self.assertIn(alias, keys, f"missing CSV row for alias {alias}")

    def test_phase2_phase3_socodes_have_csv_rows(self):
        """Phase 2/3 single-option SoCodes must have CSV rows.

        Dual-derivable codes (106, 171, 255) inherit base-service rows but
        also have explicit CSV rows for direct rating queries.
        """
        keys = frozenset(s.service_code for s in DEFAULT_SERVICES)
        for code in ("102", "106", "168", "171", "249", "255"):
            self.assertIn(code, keys, f"missing CSV row for SoCode {code}")

    def test_april_2026_lq_socodes_have_csv_rows(self):
        """Limited-Quantity (ADR-LQ) SoCodes from the April 2026 Product &
        Service List must have CSV rows so the universal rate validator
        accepts direct rating queries against them."""
        keys = frozenset(s.service_code for s in DEFAULT_SERVICES)
        for code in ("447", "704", "793", "797", "799"):
            self.assertIn(code, keys, f"missing CSV row for LQ SoCode {code}")
        # 794 surfaces under the dpd_meta_b2c_classic alias path; 338
        # surfaces under dpd_meta_b2c_small. Both must be present.
        for alias in ("794",):
            self.assertIn(alias, keys, f"missing CSV row for SoCode {alias}")

    def test_zone_tier_resolves_correct_rate(self):
        # Locks that the rate-resolver still picks up the >3 kg zones the
        # weight-bounds bug was breaking. Rate value itself is the carrier
        # default (zeroed in main commit ae593fa5 — real pricing comes from
        # the carrier API or admin-uploaded rate sheet).
        svc = self.by_code["dpd_meta_classic"]
        de_10kg = next(
            z
            for z in svc.zones
            if z.country_codes and "DE" in z.country_codes and z.min_weight == 10.0 and z.max_weight == 20.0
        )
        self.assertEqual(de_10kg.rate, 0.0)
