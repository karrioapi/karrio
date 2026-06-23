"""
Tests for the Pricing module (Markup and Fee models).

These tests cover:
1. Markup application to shipping rates (amount and percentage types)
2. Fee capture after shipment label creation
3. Various filter combinations (carrier_codes, service_codes, connection_ids)
"""

import json
import logging
from unittest.mock import ANY, patch

import karrio.server.pricing.models as models
import karrio.server.pricing.signals as signals
import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from karrio.core.models import ChargeDetails, RateDetails
from karrio.server.core import datatypes as core_datatypes
from karrio.server.core.tests import APITestCase
from karrio.server.orgs.models import Organization
from rest_framework import status

logging.disable(logging.CRITICAL)


class _StubContext:
    """Minimal stand-in for `karrio.server.serializers.Context` in pricing
    hook tests — only `org` is read by `apply_custom_markups`."""

    def __init__(self, org):
        self.org = org


class TestMarkupApplication(APITestCase):
    """Test markup application to shipping rates."""

    def setUp(self) -> None:
        super().setUp()

        # Create a markup targeting specific carriers and services
        self.markup: models.Markup = models.Markup.objects.create(
            **{
                "amount": 1.0,
                "name": "brokerage",
                "carrier_codes": ["canadapost"],
                "service_codes": ["canadapost_priority", "canadapost_regular_parcel"],
            }
        )

    def test_apply_markup_amount_to_shipment_rates(self):
        """Test applying fixed amount markup to rates."""
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_RESPONSE)

    def test_apply_markup_percentage_to_shipment_rates(self):
        """Test applying percentage markup to rates."""
        self.markup.amount = 2.0
        self.markup.markup_type = "PERCENTAGE"
        self.markup.save()
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_WITH_PERCENTAGE_RESPONSE)


class TestMarkupFilters(TestCase):
    """Test markup filter logic."""

    def test_carrier_codes_filter(self):
        """Test that markup only applies to specified carrier codes."""
        markup = models.Markup.objects.create(
            name="fedex_markup",
            amount=5.0,
            markup_type="AMOUNT",
            carrier_codes=["fedex"],
        )

        # Create mock rate for FedEx
        from karrio.server.core.datatypes import Rate, RateResponse

        fedex_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=10.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        ups_rate = Rate(
            id="rate_2",
            carrier_id="ups",
            carrier_name="ups",
            service="ups_ground",
            total_charge=12.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_456"},
        )

        response = RateResponse(
            rates=[fedex_rate, ups_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # FedEx rate should have markup applied
        fedex_result = next(r for r in result.rates if r.carrier_name == "fedex")
        self.assertEqual(fedex_result.total_charge, 15.0)  # 10 + 5

        # UPS rate should NOT have markup applied
        ups_result = next(r for r in result.rates if r.carrier_name == "ups")
        self.assertEqual(ups_result.total_charge, 12.0)  # unchanged

    def test_service_codes_filter(self):
        """Test that markup only applies to specified service codes."""
        markup = models.Markup.objects.create(
            name="express_markup",
            amount=10.0,
            markup_type="PERCENTAGE",
            service_codes=["fedex_overnight"],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        overnight_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_overnight",
            total_charge=100.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        ground_rate = Rate(
            id="rate_2",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=50.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        response = RateResponse(
            rates=[overnight_rate, ground_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Overnight rate should have 10% markup applied
        overnight_result = next(r for r in result.rates if r.service == "fedex_overnight")
        self.assertEqual(overnight_result.total_charge, 110.0)  # 100 + 10%

        # Ground rate should NOT have markup applied
        ground_result = next(r for r in result.rates if r.service == "fedex_ground")
        self.assertEqual(ground_result.total_charge, 50.0)  # unchanged

    def test_connection_ids_filter(self):
        """Test that markup only applies to specified connection IDs."""
        markup = models.Markup.objects.create(
            name="specific_connection_markup",
            amount=3.0,
            markup_type="AMOUNT",
            connection_ids=["car_special_123"],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        special_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=25.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_special_123"},
        )

        regular_rate = Rate(
            id="rate_2",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=25.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_regular_456"},
        )

        response = RateResponse(
            rates=[special_rate, regular_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Rate with special connection should have markup
        special_result = next(r for r in result.rates if r.meta.get("carrier_connection_id") == "car_special_123")
        self.assertEqual(special_result.total_charge, 28.0)  # 25 + 3

        # Rate with regular connection should NOT have markup
        regular_result = next(r for r in result.rates if r.meta.get("carrier_connection_id") == "car_regular_456")
        self.assertEqual(regular_result.total_charge, 25.0)  # unchanged

    def test_empty_filters_apply_to_all(self):
        """Test that markup with no filters applies to all rates."""
        markup = models.Markup.objects.create(
            name="global_markup",
            amount=1.0,
            markup_type="AMOUNT",
            carrier_codes=[],
            service_codes=[],
            connection_ids=[],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        rate1 = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=10.0,
            currency="USD",
            extra_charges=[],
            meta={},
        )

        rate2 = Rate(
            id="rate_2",
            carrier_id="ups",
            carrier_name="ups",
            service="ups_ground",
            total_charge=12.0,
            currency="USD",
            extra_charges=[],
            meta={},
        )

        response = RateResponse(
            rates=[rate1, rate2],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Both rates should have markup applied
        for rate in result.rates:
            if rate.carrier_name == "fedex":
                self.assertEqual(rate.total_charge, 11.0)  # 10 + 1
            elif rate.carrier_name == "ups":
                self.assertEqual(rate.total_charge, 13.0)  # 12 + 1


"""Pricing module tests."""

# ruff: noqa: S106


class TestTypedChargeBreakdown(TestCase):
    """Markup.apply_charge now emits a typed line item per markup:
    charge_type="markup" for visible, charge_type="platform_fee" for
    hidden platform fees. Customer hiding happens at the response boundary
    (fold_platform_fees_for_display) rather than by merging amounts into
    Base Charge. Invariant: sum(extra_charges) == total_charge for all
    post-hook rates."""

    def _rate(self, **overrides):
        from karrio.server.core import datatypes

        return datatypes.Rate(
            **{
                "id": "rate_1",
                "carrier_id": "dhl_parcel_de",
                "carrier_name": "dhl_parcel_de",
                "service": "dhl_parcel_de_kleinpaket",
                "total_charge": 3.43,
                "currency": "EUR",
                "extra_charges": [
                    ChargeDetails(name="Base Charge", amount=3.39, currency="EUR"),
                    ChargeDetails(name="Energy Surcharge", amount=0.04, currency="EUR"),
                ],
                "meta": {},
                **overrides,
            }
        )

    def _sum_extras(self, rate):
        return round(sum(float(c.amount or 0) for c in rate.extra_charges), 2)

    def test_invisible_markup_emits_platform_fee_line(self):
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.69,
            markup_type="AMOUNT",
            name="Shipping Start - Platform Fee",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        result = markup.apply_charge(datatypes.RateResponse(rates=[self._rate()], messages=[]))
        out = result.rates[0]

        self.assertAlmostEqual(float(out.total_charge), 4.12, places=2)
        # Plan-scoped markups always render as the canonical
        # "Platform Margin (<plan>)" line — display name is decoupled
        # from `Markup.name` so renaming the row never rewrites historical
        # or new line items.
        names = [c.name for c in out.extra_charges]
        self.assertEqual(names, ["Base Charge", "Energy Surcharge", "Platform Margin (start)"])

        platform_fee = out.extra_charges[-1]
        self.assertEqual(platform_fee.charge_type, "platform_fee")
        self.assertEqual(platform_fee.id, markup.id)
        self.assertAlmostEqual(float(platform_fee.amount), 0.69, places=2)
        self.assertEqual(platform_fee.metadata, {"plan": "start"})

        # Sum invariant
        self.assertAlmostEqual(self._sum_extras(out), float(out.total_charge), places=2)

        # Base Charge untouched — the customer-facing fold happens at the
        # response serializer, not here.
        amounts = {c.name: float(c.amount) for c in out.extra_charges}
        self.assertAlmostEqual(amounts["Base Charge"], 3.39, places=2)

    def test_visible_markup_emits_markup_line(self):
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.50,
            markup_type="AMOUNT",
            name="Coverage - 100",
            is_visible=True,
            active=True,
        )
        result = markup.apply_charge(datatypes.RateResponse(rates=[self._rate(total_charge=5.04)], messages=[]))
        out = result.rates[0]

        self.assertEqual([c.name for c in out.extra_charges], ["Base Charge", "Energy Surcharge", "Coverage - 100"])
        self.assertAlmostEqual(float(out.total_charge), 5.54, places=2)

        visible = out.extra_charges[-1]
        self.assertEqual(visible.charge_type, "markup")
        self.assertEqual(visible.id, markup.id)
        # No plan metadata for non-plan-scoped markups
        self.assertIsNone(visible.metadata)

    def test_excluded_markup_id_skips_entirely(self):
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.69,
            markup_type="AMOUNT",
            name="Shipping Start - Platform Fee",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        result = markup.apply_charge(
            datatypes.RateResponse(
                rates=[self._rate(meta={"excluded_markup_ids": [markup.id]})],
                messages=[],
            )
        )
        out = result.rates[0]

        self.assertAlmostEqual(float(out.total_charge), 3.43, places=2)
        # No platform_fee line appended.
        self.assertEqual([c.name for c in out.extra_charges], ["Base Charge", "Energy Surcharge"])

    def test_per_rate_plan_cost_slug_override(self):
        """When rate.meta carries plan_cost_<slug>, that amount wins over
        the markup's own `amount` field. This is the live-rate path today
        where the resolver stamps plan_cost amounts on meta from the rate
        sheet CSV import."""
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.0,  # sentinel — real value comes from rate.meta
            markup_type="AMOUNT",
            name="Shipping Start - Platform Fee",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        rate = self._rate(meta={"plan_cost_start": 0.81, "plan_rate_start": None})
        result = markup.apply_charge(datatypes.RateResponse(rates=[rate], messages=[]))
        out = result.rates[0]

        self.assertAlmostEqual(float(out.total_charge), 3.43 + 0.81, places=2)
        platform_fee = out.extra_charges[-1]
        self.assertEqual(platform_fee.charge_type, "platform_fee")
        self.assertAlmostEqual(float(platform_fee.amount), 0.81, places=2)
        self.assertAlmostEqual(self._sum_extras(out), float(out.total_charge), places=2)

    def test_per_rate_plan_costs_by_markup_id_override(self):
        """When rate.meta.plan_costs[<markup.id>] is set, it wins over both
        amount and plan_cost_<slug>."""
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.0,
            markup_type="AMOUNT",
            name="Shipping Start - Platform Fee",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        rate = self._rate(meta={"plan_costs": {markup.id: 1.24}, "plan_cost_types": {markup.id: "AMOUNT"}})
        result = markup.apply_charge(datatypes.RateResponse(rates=[rate], messages=[]))
        out = result.rates[0]

        self.assertAlmostEqual(float(out.total_charge), 3.43 + 1.24, places=2)
        platform_fee = out.extra_charges[-1]
        self.assertAlmostEqual(float(platform_fee.amount), 1.24, places=2)

    def test_sum_invariant_with_stacked_markups(self):
        """Applying multiple markups keeps sum(extra_charges) == total_charge."""
        from karrio.server.core import datatypes

        visible = models.Markup.objects.create(
            amount=0.50,
            markup_type="AMOUNT",
            name="Service Fee",
            is_visible=True,
            active=True,
        )
        hidden = models.Markup.objects.create(
            amount=0.81,
            markup_type="AMOUNT",
            name="Shipping Start - Platform Fee",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )
        rate = self._rate()

        # Apply sequentially
        after_visible = visible.apply_charge(datatypes.RateResponse(rates=[rate], messages=[]))
        after_hidden = hidden.apply_charge(after_visible)
        out = after_hidden.rates[0]

        self.assertAlmostEqual(self._sum_extras(out), float(out.total_charge), places=2)
        self.assertAlmostEqual(float(out.total_charge), 3.43 + 0.50 + 0.81, places=2)
        charge_types = [c.charge_type for c in out.extra_charges]
        self.assertIn("markup", charge_types)
        self.assertIn("platform_fee", charge_types)

    def test_non_applicable_rate_untouched(self):
        """Markup filtered out by carrier_codes leaves the rate untouched."""
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=5.0,
            markup_type="AMOUNT",
            name="ups-only fee",
            carrier_codes=["ups"],
            is_visible=True,
            active=True,
        )
        result = markup.apply_charge(datatypes.RateResponse(rates=[self._rate()], messages=[]))
        out = result.rates[0]

        self.assertAlmostEqual(float(out.total_charge), 3.43, places=2)
        # Original extra_charges preserved exactly.
        self.assertEqual([c.name for c in out.extra_charges], ["Base Charge", "Energy Surcharge"])
        # charge_type on the originals stays None — tagging is the resolver's job, not apply_charge's.
        self.assertIsNone(out.extra_charges[0].charge_type)

    def test_display_name_decoupled_from_markup_name(self):
        """Renaming a plan-scoped Markup row must NOT change the line item
        rendered on shipments — the admin Cost column matches by
        `charge_type` (and a stable name) and would break if every rename
        rewrote the breakdown name."""
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.50,
            markup_type="AMOUNT",
            name="Shipping Start - Platform Marin",  # historical typo
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        out = markup.apply_charge(datatypes.RateResponse(rates=[self._rate()], messages=[])).rates[0]

        platform_fee = out.extra_charges[-1]
        # Display name is the canonical synthesized form, NOT markup.name
        self.assertEqual(platform_fee.name, "Platform Margin (start)")
        self.assertEqual(platform_fee.charge_type, "platform_fee")
        self.assertEqual(platform_fee.id, markup.id)

    def test_visible_markup_keeps_admin_label(self):
        """Visible (non-plan) markups represent real merchant-facing fees
        with intentional labels — those should keep their admin name."""
        from karrio.server.core import datatypes

        markup = models.Markup.objects.create(
            amount=0.50,
            markup_type="AMOUNT",
            name="Coverage - 100",
            is_visible=True,
            active=True,
        )
        out = markup.apply_charge(datatypes.RateResponse(rates=[self._rate()], messages=[])).rates[0]

        self.assertEqual(out.extra_charges[-1].name, "Coverage - 100")
        self.assertEqual(out.extra_charges[-1].charge_type, "markup")


class TestHookResolverParity(TestCase):
    """apply_custom_markups (live-rate hook) and the resolver's
    _apply_markups_to_rates must produce structurally identical rates —
    same extra_charges shape, same meta.plan stamp, same scrubbed
    meta.plan_costs. This guards against the divergence identified in the
    2026-04-22 incident cross-check.

    Also the regression guard for SHIP2-1125 (HIGH) — cross-tier margin
    leak. Before the scrub landed on the hook path, a merchant on `start`
    could see `meta.plan_costs` and `meta.plan_cost_types` entries for
    every other tier (advanced/pro/enterprise), revealing competitor
    pricing. The scrub keeps only the active tier's entries.
    """

    def _make_org_and_markups(self):
        from karrio.server.orgs.models import Organization

        org = Organization.objects.create(name="t1", system_metadata={})  # plan unset → defaults to start
        start = models.Markup.objects.create(
            name="Shipping Start - Platform Fee",
            amount=0.0,
            markup_type="AMOUNT",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )
        pro = models.Markup.objects.create(
            name="Shipping Pro - Platform Fee",
            amount=0.0,
            markup_type="AMOUNT",
            is_visible=False,
            active=True,
            meta={"plan": "pro"},
        )
        return org, start, pro

    def _make_rate(self, markups):
        from karrio.server.core import datatypes

        return datatypes.Rate(
            id="rate_1",
            carrier_id="dhl_parcel_de",
            carrier_name="dhl_parcel_de",
            service="dhl_parcel_de_paket",
            total_charge=6.19,
            currency="EUR",
            extra_charges=[
                ChargeDetails(name="Base Charge", amount=6.00, currency="EUR"),
                ChargeDetails(name="Road Toll", amount=0.19, currency="EUR"),
            ],
            meta={
                "plan_costs": {markups[0].id: 0.81, markups[1].id: 0.50},
                "plan_cost_types": {markups[0].id: "AMOUNT", markups[1].id: "AMOUNT"},
                "plan_cost_start": 0.81,
                "plan_cost_pro": 0.50,
            },
        )

    def test_hook_stamps_plan_and_scrubs_non_active_entries(self):
        from karrio.server.core import datatypes

        class _Ctx:
            def __init__(self, org):
                self.org = org

        org, start, pro = self._make_org_and_markups()
        rate = self._make_rate([start, pro])
        result = signals.apply_custom_markups(
            datatypes.RateResponse(rates=[rate], messages=[]),
            context=_Ctx(org),
        )
        out = result.rates[0]

        # Platform fee for the active plan applied — total bumped by 0.81.
        self.assertAlmostEqual(float(out.total_charge), 6.19 + 0.81, places=2)

        # meta.plan stamped; plan_costs scrubbed to only the active markup.
        self.assertEqual(out.meta.get("plan"), "start")
        self.assertEqual(list(out.meta.get("plan_costs", {}).keys()), [start.id])
        # plan_cost_types scrubbed in lockstep — SHIP2-1125 regression guard.
        self.assertEqual(list(out.meta.get("plan_cost_types", {}).keys()), [start.id])
        # Flat `plan_cost_<slug>` extras for non-active plans stripped too.
        self.assertNotIn("plan_cost_pro", out.meta)
        self.assertIn("plan_cost_start", out.meta)
        # Pro tier's markup id is NOWHERE in the leaked meta.
        self.assertNotIn(pro.id, out.meta.get("plan_costs", {}))
        self.assertNotIn(pro.id, out.meta.get("plan_cost_types", {}))

        # Exactly one platform_fee line, none for pro.
        types = [c.charge_type for c in out.extra_charges]
        self.assertEqual(types.count("platform_fee"), 1)


def _make_live_carrier_rate(connection_id: str) -> core_datatypes.Rate:
    """Mirror what the UPS proxy + Rates.fetch returns: carrier-side meta
    only, NO plan_costs / plan_cost_<slug> keys."""
    return core_datatypes.Rate(
        id="rate_1",
        carrier_id="UPS Germany",
        carrier_name="ups",
        service="ups_standard",
        total_charge=5.53,
        currency="EUR",
        extra_charges=[
            ChargeDetails(name="BASE CHARGE", amount=4.65, currency="EUR"),
            ChargeDetails(name="MWST", amount=0.88, currency="EUR"),
        ],
        meta={
            "ext": "ups",
            "carrier": "ups",
            "rate_provider": "ups",
            "service_name": "UPS STANDARD",
            "carrier_connection_id": connection_id,
        },
    )


_DE_PAYLOAD = {
    "shipper": {"country_code": "DE"},
    "recipient": {"country_code": "DE"},
    "parcels": [{"weight": 0.27, "weight_unit": "KG"}],
}


class TestBrokeredLiveRateEnrichment(TestCase):
    """Regression guard for the 2026-05-04 UPS platform-fee = 0.0 bug.

    Live-carrier rates (Rates.fetch path) come back with carrier-side meta
    only — no rate-sheet plan_costs. Before this fix, Markup.apply_charge
    couldn't find the per-row override and fell through to Markup.amount
    (0.0 on plan-tier markups by design), so brokered shipments billed via
    a real carrier API got a 0.0 platform fee written into selected_rate.

    The hook now enriches each brokered rate's meta with the matching
    rate-sheet row's plan_costs before applying markups, bringing the
    live-carrier path into parity with the rate-sheet resolver path.
    """

    def setUp(self) -> None:
        super().setUp()
        self.org = Organization.objects.create(name="t1", system_metadata={})
        self.start_markup = models.Markup.objects.create(
            name="Shipping Start - Platform Fee",
            amount=0.0,  # mirrors prod — actual amount lives on rate-sheet rows
            markup_type="AMOUNT",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )
        self.brokered = self._make_brokered_with_row(
            row_overrides={
                "meta": {
                    "plan_costs": {self.start_markup.id: 0.54},
                    "plan_cost_types": {self.start_markup.id: "AMOUNT"},
                },
            }
        )

    def _make_brokered_with_row(self, *, row_overrides: dict) -> providers.BrokeredConnection:
        User = get_user_model()
        user = User.objects.filter(email="fee_enrich_test@example.com").first() or (
            User.objects.create_superuser("fee_enrich_test@example.com", "x")
        )
        service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            currency="EUR",
            created_by=user,
        )
        row = {
            "service_id": service.id,
            "zone_id": "zone_de",
            "rate": 4.75,
            "min_weight": 0.001,
            "max_weight": 1.001,
            **row_overrides,
        }
        sheet = providers.SystemRateSheet.objects.create(
            name="UPS DE",
            slug="ups",
            carrier_name="ups",
            zones=[{"id": "zone_de", "label": "DE", "country_codes": ["DE"]}],
            created_by=user,
            service_rates=[row],
        )
        sheet.services.add(service)
        sysconn = providers.SystemConnection.objects.create(
            carrier_code="ups", carrier_id="UPS Germany", rate_sheet=sheet
        )
        return providers.BrokeredConnection.objects.create(system_connection=sysconn)

    def _apply(self, rate: core_datatypes.Rate, payload: dict | None) -> core_datatypes.Rate:
        result = signals.apply_custom_markups(
            core_datatypes.RateResponse(rates=[rate], messages=[]),
            *([payload] if payload is not None else []),
            context=_StubContext(self.org),
        )
        return result.rates[0]

    def test_live_carrier_brokered_rate_picks_up_plan_cost_from_sheet(self):
        out = self._apply(_make_live_carrier_rate(self.brokered.system_connection_id), _DE_PAYLOAD)

        # Total bumped by 0.54 (the per-row plan_cost_start), not 0.0.
        self.assertAlmostEqual(float(out.total_charge), 5.53 + 0.54, places=2)

        # Exactly one platform_fee line, with the per-row amount (NOT 0.0).
        platform_fees = [c for c in out.extra_charges if c.charge_type == "platform_fee"]
        self.assertEqual(len(platform_fees), 1)
        self.assertAlmostEqual(float(platform_fees[0].amount), 0.54, places=2)
        self.assertEqual(platform_fees[0].id, self.start_markup.id)

        # Carrier-side extras must survive untouched — UPS billed 4.65 BASE
        # CHARGE + 0.88 MWST and we don't substitute either with the rate
        # sheet's `cost`/`rate` (4.75). We only ADD the platform markup.
        carrier_extras = [c for c in out.extra_charges if c.charge_type != "platform_fee"]
        self.assertEqual(
            [(c.name, float(c.amount)) for c in carrier_extras],
            [("BASE CHARGE", 4.65), ("MWST", 0.88)],
        )

    def test_no_payload_no_op(self):
        """When the after-hook receives no payload (some test paths), the
        enrichment must silently no-op rather than crash or guess."""
        out = self._apply(_make_live_carrier_rate(self.brokered.system_connection_id), payload=None)
        # Without recipient/parcels, enrichment can't find the row; falls
        # back to Markup.amount = 0.0, so total stays at the carrier amount.
        self.assertAlmostEqual(float(out.total_charge), 5.53, places=2)

    def test_already_enriched_meta_is_preserved(self):
        """Idempotent: if the rate already carries plan_costs, enrichment
        must not overwrite the existing values — the resolver path already
        set them and that data is authoritative."""
        rate = _make_live_carrier_rate(self.brokered.system_connection_id)
        rate.meta["plan_costs"] = {self.start_markup.id: 0.81}

        out = self._apply(rate, _DE_PAYLOAD)
        # Enrichment skipped — sheet's 0.54 NOT applied; existing 0.81 used.
        self.assertAlmostEqual(float(out.total_charge), 5.53 + 0.81, places=2)

    def test_csv_imported_flat_row_shape_resolves(self):
        """Rows imported from CSV have flat `plan_cost_<slug>` keys at the
        row level (no `meta.plan_costs`). The fallback path in
        Markup.apply_charge consumes those when no per-markup-id override
        is present — the enrichment must propagate them too."""
        # Replace the structured-meta brokered with a flat-only one.
        providers.BrokeredConnection.objects.all().delete()
        self.brokered = self._make_brokered_with_row(row_overrides={"plan_cost_start": 0.54})

        out = self._apply(_make_live_carrier_rate(self.brokered.system_connection_id), _DE_PAYLOAD)
        self.assertAlmostEqual(float(out.total_charge), 5.53 + 0.54, places=2)
        platform_fees = [c for c in out.extra_charges if c.charge_type == "platform_fee"]
        self.assertEqual(len(platform_fees), 1)
        self.assertAlmostEqual(float(platform_fees[0].amount), 0.54, places=2)


class TestStripInternalMeta(TestCase):
    """SHIP2-1125 regression guard for the active-tier leak.

    `strip_internal_meta` is the response-boundary helper called by
    `Rate.to_representation` and the shipping-methods view. It removes
    tenant-facing internal keys (plan, plan_costs, plan_cost_types,
    plan_cost_<slug>, plan_rate_<slug>) without mutating the input.
    Non-plan keys must survive untouched.
    """

    def test_strips_all_internal_plan_keys(self):
        from karrio.server.pricing.charge_breakdown import strip_internal_meta

        meta = {
            "plan": "start",
            "plan_costs": {"mkp_x": 0.81},
            "plan_cost_types": {"mkp_x": "AMOUNT"},
            "plan_cost_start": 0.81,
            "plan_rate_start": None,
            # non-plan keys — must survive
            "carrier_connection_id": "car_abc",
            "shipping_charges": 6.00,
            "ext": "dhl_parcel_de",
        }
        stripped = strip_internal_meta(meta)

        self.assertNotIn("plan", stripped)
        self.assertNotIn("plan_costs", stripped)
        self.assertNotIn("plan_cost_types", stripped)
        self.assertNotIn("plan_cost_start", stripped)
        self.assertNotIn("plan_rate_start", stripped)
        self.assertEqual(stripped["carrier_connection_id"], "car_abc")
        self.assertEqual(stripped["shipping_charges"], 6.00)
        self.assertEqual(stripped["ext"], "dhl_parcel_de")

    def test_does_not_mutate_input(self):
        from karrio.server.pricing.charge_breakdown import strip_internal_meta

        meta = {"plan": "start", "plan_costs": {"mkp_x": 0.81}, "shipping_charges": 6.00}
        strip_internal_meta(meta)
        # Input untouched.
        self.assertIn("plan", meta)
        self.assertIn("plan_costs", meta)

    def test_handles_empty_and_none(self):
        from karrio.server.pricing.charge_breakdown import strip_internal_meta

        # None passes through unchanged — callers rely on this to keep
        # "meta absent" distinct from "meta is an empty dict" in responses.
        self.assertIsNone(strip_internal_meta(None))
        self.assertEqual(strip_internal_meta({}), {})
        self.assertEqual(strip_internal_meta({"ext": "dhl"}), {"ext": "dhl"})


class TestRateResponseStripping(APITestCase):
    """SHIP2-1125 regression guard at the DRF serializer boundary.

    The `/v1/proxy/rates` endpoint must not leak internal plan/margin
    fields in `meta`. Admin callers opt out via
    `context={"include_platform_fees": True}` when invoking the
    serializer directly.
    """

    def setUp(self) -> None:
        super().setUp()
        # Seed a plan markup so the scrub + stamp runs.
        models.Markup.objects.create(
            name="Shipping Start - Platform Fee",
            amount=0.0,
            markup_type="AMOUNT",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

    def test_merchant_rate_response_meta_stripped(self):
        """Stored rate meta carries plan/plan_costs; merchant response does not."""
        url = reverse("karrio.server.proxy:shipment-rates")

        def _rate_with_plan_meta():
            from karrio.core.models import ChargeDetails

            return RateDetails(
                carrier_id="canadapost",
                carrier_name="canadapost",
                currency="CAD",
                transit_days=2,
                service="canadapost_priority",
                total_charge=100.0,
                extra_charges=[ChargeDetails(amount=100.0, currency="CAD", name="Base charge")],
                meta={
                    "ext": "canadapost",
                    "carrier": "canadapost",
                    "plan": "start",
                    "plan_costs": {"mkp_fake": 5.0},
                    "plan_cost_types": {"mkp_fake": "AMOUNT"},
                    "plan_cost_start": 5.0,
                    "shipping_charges": 100.0,
                },
            )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = ([_rate_with_plan_meta()], [])
            response = self.client.post(url, RATING_DATA)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rate = response_data["rates"][0]
        rate_meta = rate.get("meta") or {}

        # SHIP2-1125: internal plan/margin keys must NOT appear.
        self.assertNotIn("plan", rate_meta)
        self.assertNotIn("plan_costs", rate_meta)
        self.assertNotIn("plan_cost_types", rate_meta)
        self.assertNotIn("plan_cost_start", rate_meta)
        # Carrier-side meta keys survive.
        self.assertEqual(rate_meta.get("carrier"), "canadapost")
        self.assertEqual(rate_meta.get("shipping_charges"), 100.0)


class TestFeeCapture(TestCase):
    """Test fee capture after shipment creation."""

    def setUp(self):
        """Set up test data."""
        # Create a markup
        self.markup = models.Markup.objects.create(
            name="test_markup",
            amount=5.0,
            markup_type="AMOUNT",
        )

    def _make_shipment_with_org(self, **overrides):
        """Create a Shipment linked to a fresh Organization.

        Fee capture bails early when `shipment.org.first() is None` — the
        first post_save in `ShipmentSerializer.create()` fires BEFORE
        `@owned_model_serializer.link_org` writes the ShipmentLink row, so
        capture is deferred until the second save (after linking). Tests
        that go directly through `Shipment.objects.create` must link the
        org explicitly and then re-save to trigger capture.
        """
        import karrio.server.manager.models as manager
        from django.contrib.auth import get_user_model
        from karrio.server.orgs.models import Organization, ShipmentLink

        User = get_user_model()
        user = overrides.pop(
            "user",
            User.objects.create_user(email=f"fee_{id(self)}@example.com", password="x"),
        )
        org = overrides.pop(
            "org",
            Organization.objects.create(name="Fee Test Org", slug=f"fee-test-{id(self)}"),
        )
        defaults = dict(
            status="created",
            test_mode=True,
            shipper={"city": "Montreal"},
            recipient={"city": "Toronto"},
            parcels=[{"weight": 1}],
            created_by=user,
        )
        defaults.update(overrides)
        shipment = manager.Shipment.objects.create(**defaults)
        ShipmentLink.objects.create(item=shipment, org=org)
        # Re-save to re-fire post_save now that the org link exists.
        shipment.save(update_fields=["updated_at"] if "updated_at" in [f.name for f in shipment._meta.fields] else [])
        return shipment, user, org

    def test_capture_fees_from_shipment(self):
        """Test that fees are captured from shipment's selected_rate via signal.

        When a shipment is saved with status='purchased' and a selected_rate,
        the fee capture signal should automatically capture fees.
        """
        shipment, user, org = self._make_shipment_with_org(
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {
                    "carrier_code": "fedex",
                    "carrier_connection_id": "car_123",
                },
            },
        )

        # Verify fee was captured by the signal (don't call manually)
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        fee = fees.first()
        self.assertEqual(fee.markup_id, self.markup.id)
        self.assertEqual(fee.name, "test_markup")
        self.assertEqual(fee.amount, 5.0)
        self.assertEqual(fee.currency, "USD")
        self.assertEqual(fee.carrier_code, "fedex")
        self.assertEqual(fee.service_code, "fedex_ground")
        self.assertEqual(fee.connection_id, "car_123")
        self.assertEqual(fee.test_mode, True)
        # Guard for the drift we caught in admin Merchants page.
        self.assertEqual(fee.account_id, org.id)

    def test_capture_fees_function_directly(self):
        """Test the capture_fees_for_shipment function in isolation.

        Create shipment with status='draft' (so signal won't fire),
        link the org, then manually call capture function.
        """
        import karrio.server.manager.models as manager
        from django.contrib.auth import get_user_model
        from karrio.server.orgs.models import Organization, ShipmentLink

        User = get_user_model()
        user = User.objects.create_user(
            email="test_direct@example.com",
            password="testpass123",
        )
        org = Organization.objects.create(name="Direct", slug=f"direct-{id(self)}")

        # Create shipment with status that won't trigger signal
        shipment = manager.Shipment.objects.create(
            status="draft",  # Signal won't fire for this status
            test_mode=True,
            shipper={"city": "Montreal"},
            recipient={"city": "Toronto"},
            parcels=[{"weight": 1}],
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {
                    "carrier_code": "fedex",
                    "carrier_connection_id": "car_123",
                },
            },
            created_by=user,
        )
        ShipmentLink.objects.create(item=shipment, org=org)

        # No fees should exist yet
        self.assertEqual(models.Fee.objects.filter(shipment_id=shipment.id).count(), 0)

        # Manually capture fees
        signals.capture_fees_for_shipment(shipment)

        # Verify fee was captured
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        fee = fees.first()
        self.assertEqual(fee.markup_id, self.markup.id)
        self.assertEqual(fee.amount, 5.0)
        self.assertEqual(fee.account_id, org.id)

    def test_capture_fees_from_typed_platform_fee(self):
        """New typed breakdown: charge_type="platform_fee" produces a Fee row
        whose markup_id matches the charge's id. This is the primary
        post-migration path."""
        platform_markup = models.Markup.objects.create(
            name="Shipping Start - Platform Fee",
            amount=0.0,
            markup_type="AMOUNT",
            is_visible=False,
            active=True,
            meta={"plan": "start"},
        )

        shipment, user, org = self._make_shipment_with_org(
            shipper={"city": "Berlin", "country_code": "DE"},
            recipient={"city": "Munich", "country_code": "DE"},
            parcels=[{"weight": 0.5, "weight_unit": "KG"}],
            selected_rate={
                "carrier_name": "dhl_parcel_de",
                "carrier_id": "dhl_parcel_de",
                "service": "dhl_parcel_de_paket",
                "total_charge": 7.00,
                "currency": "EUR",
                "extra_charges": [
                    {"name": "Base Charge", "amount": 6.00, "currency": "EUR", "charge_type": "base"},
                    {"name": "Road Toll", "amount": 0.19, "currency": "EUR", "charge_type": "surcharge"},
                    {
                        "name": "Shipping Start - Platform Fee",
                        "amount": 0.81,
                        "currency": "EUR",
                        "id": platform_markup.id,
                        "charge_type": "platform_fee",
                        "metadata": {"plan": "start"},
                    },
                ],
                "meta": {"carrier_connection_id": "car_typed", "plan": "start"},
            },
        )

        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        fee = fees.first()
        self.assertEqual(fee.markup_id, platform_markup.id)
        self.assertEqual(fee.account_id, org.id)  # regression guard for admin Merchants stats
        self.assertAlmostEqual(fee.amount, 0.81, places=2)
        self.assertEqual(fee.currency, "EUR")
        # The Fee row survives markup deletion (no FK) — quick sanity check of the snapshot invariant.
        platform_markup.delete()
        fee.refresh_from_db()
        self.assertEqual(fee.markup_id, "mkp_" + fee.markup_id.split("_", 1)[1])  # id still present
        self.assertAlmostEqual(fee.amount, 0.81, places=2)

    def test_capture_fees_ignores_carrier_charges(self):
        """charge_type in {base, surcharge, tax} is carrier cost, not margin.
        No Fee row should be captured for those entries."""
        import karrio.server.manager.models as manager
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(email="carrier_only@example.com", password="testpass123")

        shipment = manager.Shipment.objects.create(
            status="created",
            test_mode=True,
            shipper={"city": "Berlin", "country_code": "DE"},
            recipient={"city": "Munich", "country_code": "DE"},
            parcels=[{"weight": 1.0, "weight_unit": "KG"}],
            selected_rate={
                "carrier_name": "dhl_parcel_de",
                "carrier_id": "dhl_parcel_de",
                "service": "dhl_parcel_de_paket",
                "total_charge": 7.50,
                "currency": "EUR",
                "extra_charges": [
                    {"name": "Base Charge", "amount": 7.50, "currency": "EUR", "charge_type": "base"},
                ],
                "meta": {"carrier_connection_id": "car_owncontract"},
            },
            created_by=user,
        )

        self.assertEqual(models.Fee.objects.filter(shipment_id=shipment.id).count(), 0)

    def test_no_duplicate_fee_capture(self):
        """Test that fees are not captured twice for the same shipment.

        Signal should check if fees exist before capturing.
        """
        shipment, user, org = self._make_shipment_with_org(
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {"carrier_connection_id": "car_123"},
            },
        )

        # Fee should already exist from signal
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        # Save again - signal should not create duplicate
        shipment.save()

        # Still only one fee
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

    def test_defer_capture_when_org_not_linked(self):
        """Regression guard — account_id drift in admin Merchants page.

        The first `Shipment.objects.create()` post_save fires BEFORE the
        org link is written (see @owned_model_serializer.link_org). If
        we captured a Fee at that moment its `account_id` would be NULL
        and it wouldn't count toward the admin `total_addons_charges`
        aggregate. The signal must bail early in that case and let the
        follow-up save (after link_org) complete the capture.
        """
        import karrio.server.manager.models as manager
        from django.contrib.auth import get_user_model
        from karrio.server.orgs.models import Organization, ShipmentLink

        User = get_user_model()
        user = User.objects.create_user(email="defer@example.com", password="x")

        # Step 1 — create shipment with NO org link (mirrors the pre-link
        # window during ShipmentSerializer.create).
        shipment = manager.Shipment.objects.create(
            status="created",
            test_mode=True,
            shipper={"city": "Berlin"},
            recipient={"city": "Munich"},
            parcels=[{"weight": 1}],
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {"carrier_connection_id": "car_123"},
            },
            created_by=user,
        )
        # No Fee captured yet — capture was deferred.
        self.assertEqual(models.Fee.objects.filter(shipment_id=shipment.id).count(), 0)

        # Step 2 — link org, re-save (mirrors buy_shipment_label's save).
        org = Organization.objects.create(name="Deferred", slug=f"deferred-{id(self)}")
        ShipmentLink.objects.create(item=shipment, org=org)
        shipment.save()

        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)
        self.assertEqual(fees.first().account_id, org.id)


# Test data fixtures

RATING_DATA = {
    "shipper": {
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "country_code": "CA",
        "state_code": "BC",
        "residential": True,
        "address_line1": "5840 Oak St",
    },
    "recipient": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "country_code": "CA",
        "state_code": "NB",
        "residential": False,
        "address_line1": "125 Church St",
    },
    "parcels": [
        {
            "weight": 1,
            "weight_unit": "KG",
            "packagePreset": "canadapost_corrugated_small_box",
        }
    ],
    "services": [],
    "carrier_ids": ["canadapost"],
}

RETURNED_VALUE = (
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=7,
            service="canadapost_expedited_parcel",
            total_charge=32.99,
            extra_charges=[
                ChargeDetails(amount=29.64, currency="CAD", name="Base charge"),
                ChargeDetails(amount=1.24, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-2.19, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=4.3, currency="CAD", name="Duty and taxes"),
                ChargeDetails(amount=-0.95, currency="CAD", name="Discount"),
            ],
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_xpresspost",
            total_charge=85.65,
            extra_charges=[
                ChargeDetails(amount=75.82, currency="CAD", name="Base charge"),
                ChargeDetails(amount=3.21, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-4.55, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=4.3, currency="CAD", name="Duty and taxes"),
                ChargeDetails(amount=11.17, currency="CAD", name="Discount"),
            ],
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            total_charge=113.93,
            extra_charges=[
                ChargeDetails(amount=101.83, currency="CAD", name="Base charge"),
                ChargeDetails(amount=4.27, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-7.03, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=14.86, currency="CAD", name="Duties and taxes"),
                ChargeDetails(amount=-2.76, currency="CAD", name="Discount"),
            ],
        ),
    ],
    [],
)

RATING_RESPONSE = {
    "messages": [],
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_expedited_parcel",
            "total_charge": 32.99,
            "transit_days": 7,
            "extra_charges": [
                {"name": "Base charge", "amount": 29.64, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -0.95, "currency": "CAD", "id": None},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST EXPEDITED PARCEL",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_xpresspost",
            "total_charge": 85.65,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 75.82, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": 11.17, "currency": "CAD", "id": None},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST XPRESSPOST",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 114.93,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD", "id": None},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -2.76, "currency": "CAD", "id": None},
                {"name": "brokerage", "amount": 1.0, "currency": "CAD", "id": ANY, "charge_type": "markup"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        },
    ],
}

RATING_WITH_PERCENTAGE_RESPONSE = {
    "messages": [],
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_expedited_parcel",
            "total_charge": 32.99,
            "transit_days": 7,
            "extra_charges": [
                {"name": "Base charge", "amount": 29.64, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -0.95, "currency": "CAD", "id": None},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST EXPEDITED PARCEL",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_xpresspost",
            "total_charge": 85.65,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 75.82, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": 11.17, "currency": "CAD", "id": None},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST XPRESSPOST",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 116.21,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD", "id": None},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -2.76, "currency": "CAD", "id": None},
                {"name": "brokerage", "amount": 2.28, "currency": "CAD", "id": ANY, "charge_type": "markup"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "connection_kind": "account",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        },
    ],
}


class TestNormalizeExtraCharges(TestCase):
    """`normalize_extra_charges` is the read-side adapter that lets every
    consumer (admin Cost column, billing bridge, fee capture) treat
    historical and current shipments uniformly. It must:

      - tag carrier-side entries that lack `charge_type`,
      - NOT synthesize a duplicate `platform_fee` when a typed margin
        entry is already present,
      - canonicalize plan-scoped `platform_fee` entries to the standard
        "Platform Margin (<plan>)" display name regardless of what the
        originating Markup row was called at write time.
    """

    def test_partially_typed_does_not_duplicate_platform_fee(self):
        """The post-processing hook stamps charge_type on the markup
        entry before carrier entries are typed. The adapter must not
        treat that as "untyped → synthesize" and double-count the
        margin."""
        from karrio.server.pricing.charge_breakdown import normalize_extra_charges

        selected_rate = {
            "total_charge": 6.69,
            "currency": "EUR",
            "extra_charges": [
                {"id": None, "name": "Base Charge", "amount": 6.0, "currency": "EUR"},
                {"id": None, "name": "Road Toll", "amount": 0.19, "currency": "EUR"},
                {
                    "id": "mkp_x",
                    "name": "Shipping Start - Platform Marin",
                    "amount": 0.50,
                    "currency": "EUR",
                    "metadata": {"plan": "start"},
                    "charge_type": "platform_fee",
                },
            ],
            "meta": {"plan": "start"},
        }

        out = normalize_extra_charges(selected_rate)

        platform_fees = [c for c in out if c.get("charge_type") == "platform_fee"]
        self.assertEqual(len(platform_fees), 1, "must not duplicate platform_fee")
        self.assertAlmostEqual(round(sum(float(c["amount"]) for c in out), 2), 6.69, places=2)
        # Carrier entries got tagged.
        types_by_name = {c["name"]: c.get("charge_type") for c in out}
        self.assertEqual(types_by_name["Base Charge"], "base")
        self.assertEqual(types_by_name["Road Toll"], "surcharge")
        # And the margin name was canonicalized.
        self.assertEqual(platform_fees[0]["name"], "Platform Margin (start)")

    def test_canonicalizer_strips_marin_typo(self):
        from karrio.server.pricing.charge_breakdown import _canonicalize_margin_names

        out = _canonicalize_margin_names(
            [
                {"name": "Base Charge", "charge_type": "base", "amount": 6.0},
                {
                    "name": "Shipping Start - Platform Marin",
                    "amount": 0.50,
                    "charge_type": "platform_fee",
                    "metadata": {"plan": "start"},
                },
            ]
        )
        self.assertEqual(out[1]["name"], "Platform Margin (start)")
        # Carrier entries untouched.
        self.assertEqual(out[0]["name"], "Base Charge")

    def test_synthesized_margin_uses_canonical_name(self):
        """Legacy untyped rates with carrier_sum < total still synthesize
        a platform_fee — and that synthesized line must use the canonical
        name (not 'Platform Fee (...)' from before this change)."""
        from karrio.server.pricing.charge_breakdown import normalize_extra_charges

        out = normalize_extra_charges(
            {
                "total_charge": 6.69,
                "currency": "EUR",
                "extra_charges": [
                    {"id": None, "name": "Base Charge", "amount": 6.0, "currency": "EUR"},
                    {"id": None, "name": "Road Toll", "amount": 0.19, "currency": "EUR"},
                ],
                "meta": {"plan": "start"},
            }
        )
        margin = next(c for c in out if c.get("charge_type") == "platform_fee")
        self.assertEqual(margin["name"], "Platform Margin (start)")
        self.assertAlmostEqual(margin["amount"], 0.50, places=2)


class TestMigration0083Helpers(TestCase):
    """The migration is pure-Python over JSON shapes — exercise its
    helpers directly to keep the test fast and deterministic."""

    def _migration_module(self):
        # Import via spec to bypass `0083_…` not being a valid Python
        # identifier.
        import importlib

        return importlib.import_module("karrio.server.pricing.migrations.0083_normalize_selected_rate_extra_charges")

    def test_normalize_dedupes_and_canonicalizes(self):
        m = self._migration_module()
        selected_rate = {
            "total_charge": 6.69,
            "currency": "EUR",
            "extra_charges": [
                {"id": None, "name": "Base Charge", "amount": 6.0, "currency": "EUR"},
                {"id": None, "name": "Road Toll", "amount": 0.19, "currency": "EUR"},
                {
                    "id": "mkp_x",
                    "name": "Shipping Start - Platform Marin",
                    "amount": 0.50,
                    "currency": "EUR",
                    "metadata": {"plan": "start"},
                    "charge_type": "platform_fee",
                },
                {
                    "id": "mkp_x",
                    "name": "Platform Fee (start)",
                    "amount": 0.50,
                    "currency": "EUR",
                    "metadata": {"plan": "start"},
                    "charge_type": "platform_fee",
                },
            ],
        }

        new_rate, changed = m._normalize(selected_rate)
        self.assertTrue(changed)
        extras = new_rate["extra_charges"]
        platform_fees = [c for c in extras if c.get("charge_type") == "platform_fee"]
        self.assertEqual(len(platform_fees), 1)
        self.assertEqual(platform_fees[0]["name"], "Platform Margin (start)")
        self.assertEqual(extras[0]["charge_type"], "base")
        self.assertEqual(extras[1]["charge_type"], "surcharge")
        # total_charge is authoritative — never modified.
        self.assertEqual(new_rate["total_charge"], 6.69)
        self.assertAlmostEqual(round(sum(float(c["amount"]) for c in extras), 2), 6.69, places=2)

    def test_normalize_idempotent(self):
        m = self._migration_module()
        selected_rate = {
            "total_charge": 6.69,
            "currency": "EUR",
            "extra_charges": [
                {"name": "Base Charge", "amount": 6.0, "currency": "EUR", "charge_type": "base"},
                {"name": "Road Toll", "amount": 0.19, "currency": "EUR", "charge_type": "surcharge"},
                {
                    "id": "mkp_x",
                    "name": "Platform Margin (start)",
                    "amount": 0.50,
                    "currency": "EUR",
                    "metadata": {"plan": "start"},
                    "charge_type": "platform_fee",
                },
            ],
        }
        once, changed_once = m._normalize(selected_rate)
        self.assertFalse(changed_once)
        _, changed_twice = m._normalize(once)
        self.assertFalse(changed_twice)

    def test_normalize_owncontract_no_margin(self):
        """Own-contract shipments (no plan markup) — adapter only tags
        carrier entries; no platform_fee is invented out of thin air."""
        m = self._migration_module()
        selected_rate = {
            "total_charge": 7.50,
            "currency": "EUR",
            "extra_charges": [
                {"name": "Base Charge", "amount": 7.50, "currency": "EUR"},
            ],
        }
        new_rate, changed = m._normalize(selected_rate)
        # carrier tag added → changed=True; no margin synthesized
        self.assertTrue(changed)
        extras = new_rate["extra_charges"]
        self.assertEqual(len(extras), 1)
        self.assertEqual(extras[0]["charge_type"], "base")

    def test_canonical_fee_name_plan_scoped(self):
        """Plan-scoped Fee rows normalize to 'Platform Margin (<plan>)'
        regardless of the legacy stored name."""
        m = self._migration_module()
        markup_meta_by_id = {"mkp_x": {"plan": "start"}}

        class _F:
            markup_id = "mkp_x"
            name = "Shipping Start - Platform Marin"

        self.assertEqual(m._canonical_fee_name(_F(), markup_meta_by_id), "Platform Margin (start)")

        class _G:
            markup_id = "mkp_x"
            name = "Platform Fee (start)"

        self.assertEqual(m._canonical_fee_name(_G(), markup_meta_by_id), "Platform Margin (start)")

    def test_canonical_fee_name_visible_keeps_label_with_typo_fix(self):
        """Non-plan markups keep their admin label, but the 'Marin' typo
        still gets corrected since it never represents intended text."""
        m = self._migration_module()
        markup_meta_by_id = {"mkp_y": {}}  # no plan

        class _F:
            markup_id = "mkp_y"
            name = "Coverage - 100"

        self.assertEqual(m._canonical_fee_name(_F(), markup_meta_by_id), "Coverage - 100")

        class _G:
            markup_id = "mkp_y"
            name = "Some Service - Platform Marin"

        self.assertEqual(
            m._canonical_fee_name(_G(), markup_meta_by_id),
            "Some Service - Platform Margin",
        )


class TestPlanResolvers(TestCase):
    """Verify the `plan_resolvers` hook list (used by `apply_custom_markups`)
    walks registered resolvers and returns the first truthy plan slug."""

    def test_first_resolver_wins(self):
        from karrio.server.pricing import signals as pricing_signals

        original = list(pricing_signals.plan_resolvers)
        pricing_signals.plan_resolvers[:] = [
            lambda ctx: "pro",
            lambda ctx: "should_not_be_called",
        ]
        try:
            self.assertEqual(pricing_signals._resolve_tenant_plan(None), "pro")
        finally:
            pricing_signals.plan_resolvers[:] = original

    def test_skips_resolvers_returning_none_or_empty(self):
        from karrio.server.pricing import signals as pricing_signals

        original = list(pricing_signals.plan_resolvers)
        pricing_signals.plan_resolvers[:] = [
            lambda ctx: None,
            lambda ctx: "",
            lambda ctx: "advanced",
        ]
        try:
            self.assertEqual(pricing_signals._resolve_tenant_plan(None), "advanced")
        finally:
            pricing_signals.plan_resolvers[:] = original

    def test_returns_none_when_no_resolver_registered(self):
        from karrio.server.pricing import signals as pricing_signals

        original = list(pricing_signals.plan_resolvers)
        pricing_signals.plan_resolvers[:] = []
        try:
            self.assertIsNone(pricing_signals._resolve_tenant_plan(None))
        finally:
            pricing_signals.plan_resolvers[:] = original

    def test_failing_resolver_is_isolated(self):
        """A broken extension shouldn't tank rate fetching — `lib.failsafe`
        swallows the exception and the next resolver gets a chance."""
        from karrio.server.pricing import signals as pricing_signals

        def boom(ctx):
            raise RuntimeError("resolver crashed")

        original = list(pricing_signals.plan_resolvers)
        pricing_signals.plan_resolvers[:] = [boom, lambda ctx: "start"]
        try:
            self.assertEqual(pricing_signals._resolve_tenant_plan(None), "start")
        finally:
            pricing_signals.plan_resolvers[:] = original
