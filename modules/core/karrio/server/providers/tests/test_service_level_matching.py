"""Unit tests for ServiceLevel disambiguation when variants share a code.

Mirrors the real-world UPS DE rate sheet structure:
    service_code='ups_standard' has 3 variants distinguished by features —
    "to Door" (outbound, no saturday), "to Door - Saturday" (saturday=True),
    "to Door - Return" (shipment_type=returns).

Picking the wrong variant produced 8.75 EUR base charges on shipments that
should have quoted 4.75 EUR (the saturday rate vs the standard rate).
"""

import unittest
from types import SimpleNamespace

from karrio.server.providers.service_level_matching import (
    pick_best_rate_for_method,
    pick_best_service_level,
)


def _svc(name, code, features=None, options=None):
    return SimpleNamespace(
        service_name=name,
        service_code=code,
        features=features or {},
        carrier_options=options or {},
    )


def _ups_standard_de():
    """Three same-coded variants matching the prod UPS DE rate sheet shape."""
    return [
        _svc(
            "UPS Standard to Door",
            "ups_standard",
            features={
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
                "saturday_delivery": False,
                "neighbor_delivery": False,
                "tracked": True,
            },
        ),
        _svc(
            "UPS Standard to Door - Saturday",
            "ups_standard",
            features={
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
                "saturday_delivery": True,
                "tracked": True,
            },
        ),
        _svc(
            "UPS Standard to Door - Return",
            "ups_standard",
            features={
                "shipment_type": "returns",
                "last_mile": "home_delivery",
                "saturday_delivery": False,
                "tracked": True,
            },
            options={"ups_return_of_document_indicator": True},
        ),
    ]


class TestPickBestServiceLevel(unittest.TestCase):
    def test_returns_none_when_no_code_match(self):
        services = [_svc("Express", "ups_express")]
        self.assertIsNone(pick_best_service_level(services, "ups_standard"))

    def test_returns_single_candidate_unchanged(self):
        services = [_svc("Standard", "ups_standard")]
        result = pick_best_service_level(services, "ups_standard")
        self.assertEqual(result.service_name, "Standard")

    def test_service_name_match_wins_outright(self):
        services = _ups_standard_de()
        result = pick_best_service_level(
            services,
            "ups_standard",
            service_name="UPS Standard to Door - Saturday",
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Saturday")

    def test_target_features_pick_door_variant(self):
        services = _ups_standard_de()
        # Method asks for outbound home_delivery, no saturday — Door wins.
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_features={
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
                "saturday_delivery": False,
            },
        )
        self.assertEqual(result.service_name, "UPS Standard to Door")

    def test_target_features_pick_saturday_variant(self):
        services = _ups_standard_de()
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_features={
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
                "saturday_delivery": True,
            },
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Saturday")

    def test_target_features_pick_return_variant(self):
        services = _ups_standard_de()
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_features={
                "shipment_type": "returns",
                "last_mile": "home_delivery",
            },
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Return")

    def test_target_options_disambiguate_when_features_silent(self):
        services = _ups_standard_de()
        # Method only carries the carrier option — Return variant matches.
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_options={"ups_return_of_document_indicator": True},
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Return")

    def test_silent_target_falls_back_to_canonical_door(self):
        # No target features → "off" disambiguators on Door variant make it
        # the canonical fallback (saturday_delivery=False, shipment_type=outbound).
        services = _ups_standard_de()
        result = pick_best_service_level(services, "ups_standard")
        # Without a target context the helper currently falls back to
        # alphabetical service_name ordering for determinism — "UPS Standard
        # to Door" sorts before the suffixed variants.
        self.assertEqual(result.service_name, "UPS Standard to Door")

    def test_features_as_list_normalised(self):
        services = _ups_standard_de()
        # Method.features sometimes arrives as a list of truthy flags —
        # treat ["saturday_delivery"] equivalently to {"saturday_delivery": True}.
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_features=["saturday_delivery"],
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Saturday")

    def test_conflicting_features_dock_score(self):
        services = _ups_standard_de()
        # Outbound + saturday=True + last_mile=home_delivery → Saturday variant
        # despite Return having matching shipment_type=returns mismatch.
        result = pick_best_service_level(
            services,
            "ups_standard",
            target_features={
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
                "saturday_delivery": True,
            },
        )
        self.assertEqual(result.service_name, "UPS Standard to Door - Saturday")


# ─────────────────────────────────────────────────────────────────────────────
# pick_best_rate_for_method — rate-meta side scorer
#
# Input shape matches what the SDK universal rating proxy emits after
# `lib.to_dict`: each rate is a plain dict with `service` (carrier service
# code) and `meta` carrying `service_features` (a LIST of truthy keys, not
# a dict). These tests document the False-vs-absent asymmetry vs the ORM
# scorer and exercise the witness scenario from
# shp_cc0d0501e93c4dc1850f53d5212b7b53.
# ─────────────────────────────────────────────────────────────────────────────


def _rate(name, code, features=None, options=None, **meta_extra):
    """Build a rate dict in the SDK emission shape."""
    meta = {"service_name": name}
    if features is not None:
        # SDK universal proxy emits service_features as a list of truthy keys.
        meta["service_features"] = list(features) if isinstance(features, (list, tuple, set)) else features
    if options:
        meta["carrier_options"] = options
    meta.update(meta_extra)
    return {"service": code, "meta": meta}


def _ups_standard_de_rates():
    """Three siblings sharing service_code=ups_standard — rate-meta shape.

    Mirrors the prod UPS Germany (DE) rate sheet emission for the witness
    shipment shp_cc0d0501e93c4dc1850f53d5212b7b53.
    """
    return [
        _rate(
            "UPS Standard to Door",
            "ups_standard",
            features=["b2b", "b2c", "tracked", "multicollo"],
            last_mile="home_delivery",
            shipment_type="outbound",
        ),
        _rate(
            "UPS Standard to Door - Saturday",
            "ups_standard",
            features=[
                "b2b",
                "b2c",
                "tracked",
                "multicollo",
                "saturday_delivery",
            ],
            last_mile="home_delivery",
            shipment_type="outbound",
        ),
        _rate(
            "UPS Standard to Door - Return",
            "ups_standard",
            features=["b2b", "b2c", "tracked", "multicollo"],
            options={"ups_return_of_document_indicator": True},
            last_mile="home_delivery",
            shipment_type="returns",
        ),
    ]


class TestPickBestRateForMethod(unittest.TestCase):
    def test_empty_rates_returns_none(self):
        self.assertIsNone(pick_best_rate_for_method([], "ups_standard"))

    def test_no_code_match_returns_none(self):
        rates = [_rate("Express", "ups_express", features=["express"])]
        self.assertIsNone(pick_best_rate_for_method(rates, "ups_standard"))

    def test_single_candidate_returned_unchanged(self):
        rates = [_rate("Standard", "ups_standard", features=["tracked"])]
        result = pick_best_rate_for_method(rates, "ups_standard")
        self.assertIs(result, rates[0])

    def test_method_saturday_false_picks_non_saturday(self):
        """Witness scenario: ShippingMethod opts out of Saturday — picker MUST
        return the non-Saturday sibling, not the Saturday one that happens
        to be emitted first by the SDK iterator.
        """
        rates = _ups_standard_de_rates()
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={
                "b2b": True,
                "b2c": True,
                "tracked": True,
                "multicollo": True,
                "saturday_delivery": False,
                "shipment_type": "outbound",
                "last_mile": "home_delivery",
            },
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door")

    def test_method_saturday_true_picks_saturday(self):
        rates = _ups_standard_de_rates()
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={
                "b2b": True,
                "b2c": True,
                "tracked": True,
                "saturday_delivery": True,
                "shipment_type": "outbound",
            },
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Saturday")

    def test_returns_method_picks_return_variant_via_shipment_type(self):
        rates = _ups_standard_de_rates()
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={
                "shipment_type": "returns",
                "tracked": True,
            },
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Return")

    def test_carrier_options_disambiguate_when_features_silent(self):
        rates = _ups_standard_de_rates()
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_options={"ups_return_of_document_indicator": True},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Return")

    def test_service_name_hint_wins_outright(self):
        rates = _ups_standard_de_rates()
        # Even with features that would otherwise pick the Door variant,
        # an explicit service_name hint short-circuits.
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            service_name="UPS Standard to Door - Saturday",
            target_features={"saturday_delivery": False},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Saturday")

    def test_no_context_falls_back_to_alphabetical(self):
        rates = _ups_standard_de_rates()
        # No features / options / name → deterministic alphabetical by service_name.
        result = pick_best_rate_for_method(rates, "ups_standard")
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door")

    def test_only_saturday_available_still_returns_it(self):
        # Method opts out of saturday but only the Saturday sibling is in
        # the rate list — picker still returns it (best of a bad choice)
        # rather than dropping the rate entirely. Downstream code decides
        # whether to surface a warning.
        rates = [
            _rate(
                "UPS Standard to Door - Saturday",
                "ups_standard",
                features=["saturday_delivery", "tracked"],
            ),
        ]
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={"saturday_delivery": False},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Saturday")

    def test_enum_meta_field_matched(self):
        rates = [
            _rate(
                "UPS Standard to Door",
                "ups_standard",
                features=["tracked"],
                last_mile="home_delivery",
            ),
            _rate(
                "UPS Standard to Access Point",
                "ups_standard",
                features=["tracked"],
                last_mile="service_point",
            ),
        ]
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={"last_mile": "service_point"},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Access Point")

    def test_case_insensitive_service_name_match(self):
        rates = _ups_standard_de_rates()
        # Real-world meta.service_name is sometimes uppercased downstream
        # (see witness shipment). Match should be case-insensitive.
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            service_name="UPS STANDARD TO DOOR - SATURDAY",
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Saturday")

    def test_rate_without_meta_does_not_crash(self):
        rates = [
            {"service": "ups_standard"},  # no meta at all
            _rate(
                "UPS Standard to Door",
                "ups_standard",
                features=["tracked"],
            ),
        ]
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={"tracked": True},
        )
        # The rate with the matching features wins; the malformed one
        # still participates without raising.
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door")

    def test_rate_service_none_is_filtered_out(self):
        rates = [
            {"service": None, "meta": {"service_name": "garbage"}},
            _rate(
                "UPS Standard to Door",
                "ups_standard",
                features=["tracked"],
            ),
        ]
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features={"tracked": True},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door")

    def test_features_as_list_target_normalised(self):
        # method.features sometimes arrives as a list (legacy callers).
        rates = _ups_standard_de_rates()
        result = pick_best_rate_for_method(
            rates,
            "ups_standard",
            target_features=["saturday_delivery"],
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Saturday")


# ─────────────────────────────────────────────────────────────────────────────
# Alias-aware matching — closes shp_e502d4fdb3ac48d08791b15b46c790a8 where the
# method's service_code `ups_express_pl` failed to match a live UPS rate
# labelled `ups_express` because the rate parser canonicalizes zone-suffixed
# aliases via `ServiceZone._ZONE_ALIAS_TO_BASE`. The matcher resolves both
# names through `karrio.providers.<carrier>.units.ServiceCode` and considers
# them equivalent when they map to the same wire code (both "07" here).
# ─────────────────────────────────────────────────────────────────────────────


class TestPickBestRateForMethodAliasFallback(unittest.TestCase):
    def _rate_with_carrier(self, name, code, carrier_name="ups", **kw):
        rate = _rate(name, code, **kw)
        rate["carrier_name"] = carrier_name
        return rate

    def test_zone_suffixed_alias_matches_canonical_rate(self):
        # Reproduces the prod failure: user/method selected `ups_express_pl`
        # (DE → AU via UPSExpress-Cloud), UPS returned code "07" which the
        # parser canonicalized to `ups_express`. Pre-fix this raised
        # "service not available". Post-fix the alias resolves through
        # ServiceCode (ups_express_pl = ups_express = "07") and matches.
        rates = [
            self._rate_with_carrier("UPS Express", "ups_express", features=["tracked"]),
        ]
        result = pick_best_rate_for_method(rates, "ups_express_pl")
        self.assertIsNotNone(result)
        self.assertEqual(result["service"], "ups_express")

    def test_alias_does_not_match_unrelated_service(self):
        # `ups_standard` (code "11") must not match a rate labelled
        # `ups_express` (code "07") even via the alias path.
        rates = [
            self._rate_with_carrier("UPS Express", "ups_express", features=["tracked"]),
        ]
        self.assertIsNone(pick_best_rate_for_method(rates, "ups_standard"))

    def test_alias_fallback_skipped_when_exact_match_exists(self):
        # Sanity: when the exact-name rate is present, alias siblings must
        # not be considered (otherwise we'd widen the candidate pool and
        # let the scorer pick a wrong sibling). The exact-match `ups_express`
        # rate wins outright.
        rates = [
            self._rate_with_carrier("UPS Express", "ups_express", features=["tracked"]),
            self._rate_with_carrier("UPS Express PL", "ups_express_pl", features=["tracked"]),
        ]
        result = pick_best_rate_for_method(rates, "ups_express_pl")
        self.assertEqual(result["service"], "ups_express_pl")

    def test_no_carrier_name_falls_through(self):
        # Rate dict missing `carrier_name` — the alias lookup is keyed on
        # carrier, so missing carrier means no alias resolution. Behaviour
        # equals the pre-fix exact-match path.
        rates = [_rate("UPS Express", "ups_express", features=["tracked"])]
        self.assertIsNone(pick_best_rate_for_method(rates, "ups_express_pl"))

    def test_unknown_carrier_does_not_crash(self):
        # Carrier module not importable → alias map is empty → fallback
        # returns no match, but never raises. (No regression for carriers
        # without a ServiceCode enum, which is 24 of 26 connectors.)
        rates = [self._rate_with_carrier("X", "service_a", carrier_name="not_a_real_carrier")]
        self.assertIsNone(pick_best_rate_for_method(rates, "service_b"))

    def test_alias_match_with_variant_scoring(self):
        # When alias-matched candidates contain sibling variants (same
        # service_code, different features), the variant scorer still
        # picks the right one based on target_features. This proves the
        # alias fallback composes with the existing scoring pipeline.
        rates = [
            self._rate_with_carrier(
                "UPS Standard to Door",
                "ups_standard",
                features=["tracked"],
                shipment_type="outbound",
            ),
            self._rate_with_carrier(
                "UPS Standard to Door - Return",
                "ups_standard",
                features=["tracked"],
                shipment_type="returns",
            ),
        ]
        result = pick_best_rate_for_method(
            rates,
            "ups_standard_pl",
            target_features={"shipment_type": "returns", "tracked": True},
        )
        self.assertEqual(result["meta"]["service_name"], "UPS Standard to Door - Return")
