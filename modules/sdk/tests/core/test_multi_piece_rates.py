"""Regression tests for `to_multi_piece_rates` variant disambiguation.

When multiple ServiceLevels share a carrier `service_code` (e.g. UPS Standard
to Door / Saturday / Return all carry `ups_standard` because UPS defines one
code 11 — saturday is a request option, return is a return-service option),
the rate-aggregation step must not collapse them. Each variant is identified
by its `(service_code, service_name)` tuple — `rate_variant_key` returns
this; `to_multi_piece_rates` keys on it for grouping across packages.

A prior version of `to_multi_piece_rates` keyed on bare `rate.service`. For
the single-piece path that meant `next((r for r in rates if r.service == main.service))`
returned the FIRST sibling for every `main` — so Saturday/Return/Standard
all ended up with Saturday's `total_charge` + `extra_charges` glued onto
their own `meta`. Live UPS DE shipments routinely quoted the saturday rate
(8.75 EUR base) instead of the standard rate (4.75 EUR) as a result.
"""

import unittest

import karrio.core.models as models
from karrio.core.utils.transformer import rate_variant_key, to_multi_piece_rates


def _make_rate(
    service_code: str,
    service_name: str,
    base_charge: float,
    total_charge: float | None = None,
    currency: str = "EUR",
) -> models.RateDetails:
    return models.RateDetails(
        carrier_name="ups",
        carrier_id="UPS Germany",
        service=service_code,
        currency=currency,
        total_charge=total_charge if total_charge is not None else base_charge,
        extra_charges=[
            models.ChargeDetails(name="Base Charge", amount=base_charge, currency=currency),
        ],
        meta={
            "service_name": service_name,
            "shipping_charges": base_charge,
        },
    )


class TestRateVariantKey(unittest.TestCase):
    def test_returns_service_code_and_service_name_tuple(self):
        rate = _make_rate("ups_standard", "UPS Standard to Door", 4.75)
        self.assertEqual(
            rate_variant_key(rate),
            ("ups_standard", "UPS Standard to Door"),
        )

    def test_missing_service_name_falls_back_to_empty_string(self):
        rate = _make_rate("ups_standard", "", 4.75)
        rate.meta = None
        self.assertEqual(rate_variant_key(rate), ("ups_standard", ""))

    def test_strips_whitespace_in_service_name(self):
        rate = _make_rate("ups_standard", "  UPS Standard to Door  ", 4.75)
        self.assertEqual(
            rate_variant_key(rate),
            ("ups_standard", "UPS Standard to Door"),
        )


class TestToMultiPieceRatesVariantAggregation(unittest.TestCase):
    """UPS DE has three ServiceLevels under `service_code=ups_standard`:
    Saturday (8.75), Return (4.75), Standard to Door (4.75). They must not
    collapse during aggregation."""

    def setUp(self):
        self.maxDiff = None
        self.saturday = _make_rate("ups_standard", "UPS Standard to Door - Saturday", 8.75)
        self.returning = _make_rate("ups_standard", "UPS Standard to Door - Return", 4.75)
        self.standard = _make_rate("ups_standard", "UPS Standard to Door", 4.75)

    def test_single_piece_preserves_variant_identity(self):
        """Each variant survives aggregation with its own charges + total."""
        result = to_multi_piece_rates([("pkg_1", [self.saturday, self.returning, self.standard])])
        self.assertEqual(len(result), 3)

        by_name = {(r.meta or {}).get("service_name"): r for r in result}
        self.assertEqual(by_name["UPS Standard to Door - Saturday"].total_charge, 8.75)
        self.assertEqual(by_name["UPS Standard to Door - Saturday"].extra_charges[0].amount, 8.75)
        self.assertEqual(by_name["UPS Standard to Door - Return"].total_charge, 4.75)
        self.assertEqual(by_name["UPS Standard to Door - Return"].extra_charges[0].amount, 4.75)
        self.assertEqual(by_name["UPS Standard to Door"].total_charge, 4.75)
        self.assertEqual(by_name["UPS Standard to Door"].extra_charges[0].amount, 4.75)

    def test_multi_piece_sums_per_variant(self):
        """Two packages, two variants each: per-variant totals sum across
        packages; siblings do NOT bleed into each other."""
        sat_pkg2 = _make_rate("ups_standard", "UPS Standard to Door - Saturday", 8.75)
        std_pkg2 = _make_rate("ups_standard", "UPS Standard to Door", 4.75)
        result = to_multi_piece_rates(
            [
                ("pkg_1", [self.saturday, self.standard]),
                ("pkg_2", [sat_pkg2, std_pkg2]),
            ]
        )
        self.assertEqual(len(result), 2)

        by_name = {(r.meta or {}).get("service_name"): r for r in result}
        self.assertEqual(by_name["UPS Standard to Door - Saturday"].total_charge, 17.5)
        self.assertEqual(by_name["UPS Standard to Door - Saturday"].extra_charges[0].amount, 17.5)
        self.assertEqual(by_name["UPS Standard to Door"].total_charge, 9.5)
        self.assertEqual(by_name["UPS Standard to Door"].extra_charges[0].amount, 9.5)

    def test_variant_only_on_one_piece_is_dropped(self):
        """If a variant doesn't appear on every package, aggregation skips it
        (existing all-or-nothing semantic)."""
        sat_pkg2 = _make_rate("ups_standard", "UPS Standard to Door - Saturday", 8.75)
        # pkg_2 only has Saturday, not Standard:
        result = to_multi_piece_rates(
            [
                ("pkg_1", [self.saturday, self.standard]),
                ("pkg_2", [sat_pkg2]),
            ]
        )
        # main_piece_rates comes from pkg_1 (max=2). Saturday survives
        # because pkg_2 has it. Standard is dropped because pkg_2 lacks it.
        self.assertEqual(len(result), 1)
        self.assertEqual((result[0].meta or {}).get("service_name"), "UPS Standard to Door - Saturday")

    def test_single_variant_unaffected(self):
        """The common single-variant case (no service_code collisions) still
        works — backward compatibility check."""
        rate1 = _make_rate("dhl_paket", "DHL Paket", 6.99)
        rate2 = _make_rate("dhl_paket", "DHL Paket", 6.99)
        result = to_multi_piece_rates([("pkg_1", [rate1]), ("pkg_2", [rate2])])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].total_charge, 13.98)
        self.assertEqual(result[0].extra_charges[0].amount, 13.98)

    def test_empty_input(self):
        self.assertEqual(to_multi_piece_rates([]), [])


if __name__ == "__main__":
    unittest.main()
