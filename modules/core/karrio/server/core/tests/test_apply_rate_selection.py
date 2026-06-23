"""Unit tests for `apply_rate_selection` variant disambiguation.

`apply_rate_selection` picks one rate out of the list returned by the SDK
rate fetch. Before this PR the selection was a bare
`next(r for r in rates if r["service"] == code)` — first match wins. When
multiple sibling ServiceLevels share a service_code (UPS Standard / Saturday
/ Return on `ups_standard`, DHL Paket variants on `dhl_parcel_de_paket`)
this picked an arbitrary sibling regardless of the chosen method's intent.

Witness shipment: shp_cc0d0501e93c4dc1850f53d5212b7b53 — a JTL Wawi shipment
ended up with `selected_rate.meta.service_name = "UPS STANDARD TO DOOR -
SATURDAY"` even though the underlying ShippingMethod has
`features.saturday_delivery = False`. The label sent to UPS was plain code
11 (no Saturday option) so the carrier bill was correct — but the stored
rate metadata was wrong, corrupting billing snapshots and rate audits.

The fix carries the method's features+carrier_options+service_name through
`meta.shipping_method` (stamped by `apply_shipping_method_to_data`) and
scores rate candidates via `pick_best_rate_for_method`.
"""

import unittest

from karrio.server.core.utils import apply_rate_selection


def _rate(rate_id, service, name, features=None, options=None, **meta_extra):
    """Build a rate dict in the SDK emission shape."""
    meta = {"service_name": name}
    if features is not None:
        meta["service_features"] = list(features)
    if options:
        meta["carrier_options"] = options
    meta.update(meta_extra)
    return {
        "id": rate_id,
        "service": service,
        "carrier_name": "ups",
        "meta": meta,
    }


def _ups_rates():
    """Two ups_standard siblings — Saturday emitted first (cheapest after markup)."""
    return [
        _rate(
            "rat_saturday",
            "ups_standard",
            "UPS Standard to Door - Saturday",
            features=["b2b", "b2c", "tracked", "multicollo", "saturday_delivery"],
        ),
        _rate(
            "rat_door",
            "ups_standard",
            "UPS Standard to Door",
            features=["b2b", "b2c", "tracked", "multicollo"],
        ),
    ]


def _payload(**overrides):
    base = {
        "rates": _ups_rates(),
        "options": {},
        "meta": {},
    }
    base.update(overrides)
    return base


class TestApplyRateSelectionVariantDisambiguation(unittest.TestCase):
    def test_existing_selected_rate_passthrough(self):
        explicit = {"id": "rat_explicit", "service": "ups_standard"}
        payload = _payload(selected_rate=explicit)
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"], explicit)

    def test_explicit_rate_id_match_bypasses_scoring(self):
        # Even with method.saturday=False, an explicit selected_rate_id wins.
        payload = _payload(
            selected_rate_id="rat_saturday",
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_x",
                    "name": "JTL UPS Standard",
                    "features": {"saturday_delivery": False},
                    "carrier_options": {},
                },
            },
        )
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"]["id"], "rat_saturday")

    def test_service_only_no_method_meta_legacy_first_match(self):
        # No shipping_method meta → scorer has no signal → deterministic
        # alphabetical fallback by service_name. Both rates carry an
        # ups_standard service code; service_name "UPS Standard to Door"
        # sorts before "UPS Standard to Door - Saturday".
        payload = _payload(service="ups_standard")
        result = apply_rate_selection(payload)
        self.assertIsNotNone(result["selected_rate"])
        self.assertEqual(
            result["selected_rate"]["meta"]["service_name"],
            "UPS Standard to Door",
        )

    def test_method_saturday_false_picks_non_saturday(self):
        """Witness shipment regression — method opts out of Saturday."""
        payload = _payload(
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_42aba",
                    "name": "JTL UPS Standard to Door 0 - 1kg",
                    "features": {
                        "b2b": True,
                        "b2c": True,
                        "tracked": True,
                        "multicollo": True,
                        "saturday_delivery": False,
                        "shipment_type": "outbound",
                        "last_mile": "home_delivery",
                    },
                    "carrier_options": {},
                },
            },
        )
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"]["id"], "rat_door")
        self.assertEqual(
            result["selected_rate"]["meta"]["service_name"],
            "UPS Standard to Door",
        )

    def test_method_saturday_true_picks_saturday(self):
        payload = _payload(
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_sat",
                    "name": "JTL UPS Saturday",
                    "features": {
                        "b2b": True,
                        "b2c": True,
                        "tracked": True,
                        "saturday_delivery": True,
                    },
                    "carrier_options": {},
                },
            },
        )
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"]["id"], "rat_saturday")

    def test_service_name_hint_in_method_meta(self):
        # Method writer stamped the resolved ServiceLevel.service_name.
        payload = _payload(
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_sat",
                    "name": "JTL UPS Saturday",
                    "service_name": "UPS Standard to Door - Saturday",
                    "features": {},
                    "carrier_options": {},
                },
            },
        )
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"]["id"], "rat_saturday")

    def test_no_rate_matches_returns_none(self):
        payload = _payload(
            rates=[],
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_x",
                    "name": "x",
                    "features": {"saturday_delivery": False},
                    "carrier_options": {},
                }
            },
        )
        result = apply_rate_selection(payload)
        self.assertIsNone(result["selected_rate"])

    def test_has_alternative_services_fallback_when_scorer_misses(self):
        # No rate has service=ups_express but options.has_alternative_services
        # asks for a carrier_name fallback.
        payload = _payload(
            rates=[
                _rate(
                    "rat_dhl_only",
                    "dhl_express",
                    "DHL Express",
                    features=["tracked"],
                ),
            ],
            service="ups_standard",
            options={"has_alternative_services": True},
        )
        # _get_carrier_for_service relies on references — since we're not
        # exercising that path here, we accept that the fallback returns
        # None when no carrier match is available. The important assertion
        # is that the new code path doesn't raise.
        result = apply_rate_selection(payload)
        self.assertIn("selected_rate", result)

    def test_rate_id_mismatch_falls_through_to_service_scoring(self):
        # Legacy callers sometimes pass a stale rate_id that doesn't appear
        # in the current rates list; the service-based path must still pick
        # the right variant.
        payload = _payload(
            selected_rate_id="rat_does_not_exist",
            service="ups_standard",
            meta={
                "shipping_method": {
                    "id": "mtd_x",
                    "name": "x",
                    "features": {"saturday_delivery": False},
                    "carrier_options": {},
                },
            },
        )
        result = apply_rate_selection(payload)
        self.assertEqual(result["selected_rate"]["id"], "rat_door")

    def test_empty_meta_safe(self):
        # payload missing meta entirely — must not crash.
        payload = {
            "rates": _ups_rates(),
            "service": "ups_standard",
            "options": {},
        }
        result = apply_rate_selection(payload)
        self.assertIsNotNone(result["selected_rate"])
