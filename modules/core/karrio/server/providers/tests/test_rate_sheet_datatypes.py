"""Unit tests for rate sheet typed datatypes.

These assert round-trip semantics (dict → typed → dict must preserve the
storage shape) so the refactor stays behavior-preserving across all
consumers of `rate_sheet.service_rates`, `.zones`, `.surcharges`, etc.
"""

import unittest

from karrio.server.providers.rate_sheet_datatypes import (
    PlanOverride,
    RateRowMeta,
    RateSheetPricingConfig,
    ServiceMetadata,
    ServiceRateRow,
    SurchargeDef,
    ZoneDef,
)


class TestPlanOverride(unittest.TestCase):
    def test_empty_override_returns_none_tuple(self):
        self.assertEqual(PlanOverride().override_for("mkp_xxx"), (None, None))
        self.assertTrue(PlanOverride().is_empty())

    def test_override_for_returns_amount_and_type(self):
        po = PlanOverride(
            plan_costs={"mkp_a": 4.25, "mkp_b": 1.5},
            plan_cost_types={"mkp_a": "AMOUNT", "mkp_b": "PERCENTAGE"},
        )
        self.assertEqual(po.override_for("mkp_a"), (4.25, "AMOUNT"))
        self.assertEqual(po.override_for("mkp_b"), (1.5, "PERCENTAGE"))
        self.assertEqual(po.override_for("mkp_missing"), (None, None))

    def test_from_dict_accepts_none(self):
        self.assertTrue(PlanOverride.from_dict(None).is_empty())
        self.assertTrue(PlanOverride.from_dict({}).is_empty())

    def test_from_dict_reads_plan_costs(self):
        po = PlanOverride.from_dict({"plan_costs": {"mkp_a": 4.25}, "plan_cost_types": {"mkp_a": "AMOUNT"}})
        self.assertEqual(po.override_for("mkp_a"), (4.25, "AMOUNT"))


class TestRateRowMeta(unittest.TestCase):
    def test_round_trip_preserves_storage_shape(self):
        source = {
            "fuel_surcharge": 1.5,
            "plan_rate_start": 4.08,
            "plan_costs": {"mkp_a": 4.25},
            "plan_cost_types": {"mkp_a": "AMOUNT"},
            "transit_time": "best_effort",
            "excluded_markup_ids": ["mkp_b"],
            "age_check": True,  # carrier-specific extra
        }
        round_tripped = RateRowMeta.from_dict(source).to_dict()
        self.assertEqual(round_tripped["fuel_surcharge"], 1.5)
        self.assertEqual(round_tripped["plan_rate_start"], 4.08)
        self.assertEqual(round_tripped["plan_costs"], {"mkp_a": 4.25})
        self.assertEqual(round_tripped["plan_cost_types"], {"mkp_a": "AMOUNT"})
        self.assertEqual(round_tripped["transit_time"], "best_effort")
        self.assertEqual(round_tripped["excluded_markup_ids"], ["mkp_b"])
        self.assertTrue(round_tripped["age_check"])

    def test_empty_meta_round_trips_to_empty_dict(self):
        self.assertEqual(RateRowMeta.from_dict(None).to_dict(), {})
        self.assertEqual(RateRowMeta.from_dict({}).to_dict(), {})

    def test_plan_override_helper_matches_stored_shape(self):
        meta = RateRowMeta.from_dict({"plan_costs": {"mkp_a": 4.25}, "plan_cost_types": {"mkp_a": "AMOUNT"}})
        self.assertEqual(meta.plan_override.override_for("mkp_a"), (4.25, "AMOUNT"))


class TestServiceRateRow(unittest.TestCase):
    def test_round_trip(self):
        source = {
            "service_id": "svc_x",
            "zone_id": "zone_de",
            "rate": 10.0,
            "min_weight": 0,
            "max_weight": 5,
            "meta": {"plan_costs": {"mkp_a": 4.25}, "plan_cost_types": {"mkp_a": "AMOUNT"}},
        }
        row = ServiceRateRow.from_dict(source)
        self.assertEqual(row.service_id, "svc_x")
        self.assertEqual(row.meta.plan_override.override_for("mkp_a"), (4.25, "AMOUNT"))

        rt = row.to_dict()
        self.assertEqual(rt["service_id"], "svc_x")
        self.assertEqual(rt["rate"], 10.0)
        self.assertEqual(rt["meta"]["plan_costs"], {"mkp_a": 4.25})


class TestZoneDef(unittest.TestCase):
    def test_round_trip(self):
        source = {
            "id": "zone_de",
            "label": "Germany",
            "country_codes": ["DE"],
            "transit_days": 2,
        }
        rt = ZoneDef.from_dict(source).to_dict()
        self.assertEqual(rt["id"], "zone_de")
        self.assertEqual(rt["country_codes"], ["DE"])
        self.assertEqual(rt["transit_days"], 2)


class TestSurchargeDef(unittest.TestCase):
    def test_round_trip(self):
        source = {
            "id": "chrg_x",
            "name": "Fuel",
            "amount": 2.5,
            "surcharge_type": "AMOUNT",
            "active": True,
        }
        rt = SurchargeDef.from_dict(source).to_dict()
        self.assertEqual(rt, {**source})


class TestServiceMetadata(unittest.TestCase):
    def test_shipping_method_lifts_to_top_level(self):
        rt = ServiceMetadata.from_dict({"shipping_method": "DHL Paket"}).to_dict()
        self.assertEqual(rt, {"shipping_method": "DHL Paket"})

    def test_extras_preserved(self):
        rt = ServiceMetadata.from_dict({"shipping_method": "DHL", "foo": "bar"}).to_dict()
        self.assertEqual(rt, {"shipping_method": "DHL", "foo": "bar"})

    def test_empty(self):
        self.assertEqual(ServiceMetadata.from_dict(None).to_dict(), {})


class TestRateSheetPricingConfig(unittest.TestCase):
    def test_round_trip(self):
        rt = RateSheetPricingConfig.from_dict({"excluded_markup_ids": ["mkp_a"], "sort_order": 3}).to_dict()
        self.assertEqual(rt, {"excluded_markup_ids": ["mkp_a"], "sort_order": 3})

    def test_empty_round_trips_to_empty_dict(self):
        self.assertEqual(RateSheetPricingConfig.from_dict(None).to_dict(), {})
