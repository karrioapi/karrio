"""
Charge-breakdown adapter.

Downstream consumers (billing bridge, fee capture, admin analytics) read
`shipment.selected_rate.extra_charges` expecting a typed shape: every entry
carries a `charge_type` and `sum(amount) == total_charge`.

Rates emitted by Markup.apply_charge and the shipping method rate
resolver after this change already carry that shape. Shipments purchased
before the change have one of two legacy shapes:

1. Non-folded (live-rate path pre-fix): carrier-side extras only, markup
   bumped total_charge without updating extras. `sum(extras) != total`.
2. Folded (resolver path pre-fix): markup amount merged INTO the existing
   Base Charge entry. `sum(extras) == total` but no way to distinguish
   carrier cost from JTL margin.

This module reconstructs the typed breakdown from either legacy shape so
consumers can use one code path against every historical shipment without
a data migration.
"""

from __future__ import annotations

import copy
import logging
import typing

logger = logging.getLogger(__name__)


CARRIER_CHARGE_TYPES = ("base", "surcharge", "tax")
MARGIN_CHARGE_TYPES = ("markup", "platform_fee")


def _is_typed(extra_charges: list[dict]) -> bool:
    """True when every entry already has a non-null charge_type."""
    return bool(extra_charges) and all(c.get("charge_type") for c in extra_charges)


def _resolve_active_markup_id(
    meta: dict,
    org_plan: str | None,
) -> tuple[str | None, float | None]:
    """Return (markup_id, amount) for the plan markup that applies to this rate.

    Strategy, in order:
      1. `meta.plan_costs` with a single entry → that is the scrubbed
         active entry (produced by either the resolver or, now, the hook).
      2. `meta.plan_costs` with multiple entries → find the one whose
         `mkp_id` matches a markup whose `meta.plan == org_plan`.
         Falls back to None if we cannot be sure.
      3. Flat `plan_cost_<plan>` key → use that amount, markup_id unknown
         (returned as None).
    """
    plan_costs = meta.get("plan_costs")
    if isinstance(plan_costs, dict) and len(plan_costs) == 1:
        mkp_id, amount = next(iter(plan_costs.items()))
        return mkp_id, amount

    if isinstance(plan_costs, dict) and org_plan:
        # Avoid a DB lookup in hot paths — resolve markup ids by importing
        # Markup lazily only when needed.
        try:
            from karrio.server.pricing.models import Markup

            for mkp_id in plan_costs:
                mk = Markup.objects.filter(id=mkp_id).only("id", "meta").first()
                if mk and (mk.meta or {}).get("plan") == org_plan:
                    return mkp_id, plan_costs[mkp_id]
        except Exception as exc:  # pragma: no cover — defensive, ORM unavailable in SDK-only calls
            logger.debug("charge_breakdown: markup lookup skipped (%s)", exc)

    if org_plan:
        slug_amount = meta.get(f"plan_cost_{org_plan}")
        if slug_amount is not None:
            return None, float(slug_amount)

    return None, None


def _tag_carrier_entries(extra_charges: list[dict]) -> list[dict]:
    """Tag untyped entries using legacy id-prefix heuristics + positional fallback.

    - `id` starts with `mkp_` → `markup` (merchant-visible margin).
    - `id` starts with `chrg_` → `markup` (legacy Surcharge ids).
    - Otherwise, first entry → `base`, subsequent → `surcharge`.
    """
    result = []
    base_assigned = False
    for entry in extra_charges:
        new_entry = dict(entry)
        if not new_entry.get("charge_type"):
            entry_id = new_entry.get("id") or ""
            if entry_id.startswith(("mkp_", "chrg_")):
                new_entry["charge_type"] = "markup"
            elif not base_assigned:
                new_entry["charge_type"] = "base"
            else:
                new_entry["charge_type"] = "surcharge"
        if new_entry["charge_type"] == "base":
            base_assigned = True
        result.append(new_entry)
    return result


def normalize_extra_charges(
    selected_rate: dict | None,
    org_plan: str | None = None,
) -> list[dict]:
    """Return a typed extra_charges list for any historical or current shape.

    The returned list is a deep copy — the input is never mutated. Each
    entry has a `charge_type` set to one of:
      base | surcharge | tax | markup | platform_fee | addon

    Post-condition (when reconstruction succeeds):
      round(sum(amount), 2) == round(total_charge, 2)

    When reconstruction cannot be done confidently (missing meta, unknown
    shape), this helper falls back to tagging the existing entries without
    synthesizing any platform_fee line. Callers should treat such rates as
    "no JTL margin captured on this row" rather than failing.
    """
    if not selected_rate:
        return []

    extra_charges = list(selected_rate.get("extra_charges") or [])
    extra_charges = [copy.deepcopy(c) for c in extra_charges]

    if _is_typed(extra_charges):
        return extra_charges

    total_charge = float(selected_rate.get("total_charge") or 0)
    meta = selected_rate.get("meta") or {}
    currency = selected_rate.get("currency") or "EUR"
    # Prefer the stamped plan on the rate meta — the hook and resolver
    # both set this now. Fall back to the caller-provided org_plan
    # (used for pre-stamp shipments).
    active_plan = meta.get("plan") or org_plan

    # Tag existing entries as base/surcharge so we can reason about the
    # carrier side.
    tagged = _tag_carrier_entries(extra_charges)
    carrier_sum = round(
        sum(float(c.get("amount") or 0) for c in tagged if c.get("charge_type") in CARRIER_CHARGE_TYPES),
        2,
    )
    delta = round(total_charge - carrier_sum, 2)

    # Existing margin entry (added by the rate post-processing hook before
    # carrier-side entries were typed). When present, it already accounts
    # for `delta`; synthesizing another would double-count the margin and
    # break `sum(extras) == total_charge`.
    existing_margin = round(
        sum(float(c.get("amount") or 0) for c in tagged if c.get("charge_type") in MARGIN_CHARGE_TYPES),
        2,
    )
    if existing_margin > 0 and abs(round(carrier_sum + existing_margin - total_charge, 2)) < 0.005:
        return _canonicalize_margin_names(tagged)

    if abs(delta) < 0.005:
        # Shape B handled: either own-contract (no margin) or the folded
        # shape with the full total already in base+surcharge. We can't
        # tell those apart without more context, so we try to split the
        # Base Charge if the rate clearly carries a plan markup.
        return _split_folded_base_charge(tagged, meta, active_plan, currency) or tagged

    # Shape A (non-folded): carrier_sum < total. Synthesize the missing
    # platform_fee line. If the plan markup id is recoverable from meta,
    # use it; otherwise tag by plan slug only.
    markup_id, _ = _resolve_active_markup_id(meta, active_plan)
    platform_fee_entry = {
        "name": f"Platform Margin ({active_plan})" if active_plan else "Platform Margin",
        "amount": delta,
        "currency": currency,
        "id": markup_id,
        "charge_type": "platform_fee",
        **({"metadata": {"plan": active_plan}} if active_plan else {}),
    }
    return [*tagged, platform_fee_entry]


def _canonicalize_margin_names(extra_charges: list[dict]) -> list[dict]:
    """Rewrite plan-scoped platform_fee entries to the canonical display name.

    Source of truth for "is this margin?" is `charge_type` — the name is
    purely cosmetic. We standardize plan-scoped entries to
    `Platform Margin (<plan>)` so historical shipments and new shipments
    render the same way regardless of what the originating Markup row was
    called at write time.
    """
    result = []
    for entry in extra_charges:
        if entry.get("charge_type") != "platform_fee":
            result.append(entry)
            continue
        plan = (entry.get("metadata") or {}).get("plan")
        new_entry = dict(entry)
        new_entry["name"] = f"Platform Margin ({plan})" if plan else "Platform Margin"
        result.append(new_entry)
    return result


def _split_folded_base_charge(
    tagged: list[dict],
    meta: dict,
    active_plan: str | None,
    currency: str,
) -> list[dict] | None:
    """If the Base Charge entry has plan markup merged into it, split it.

    Returns a new list with a reduced Base Charge and a synthesized
    platform_fee entry. Returns None when no split is possible (no plan
    signal in meta — shipment is own-contract and the folded shape is
    actually just carrier side).
    """
    markup_id, markup_amount = _resolve_active_markup_id(meta, active_plan)
    if markup_amount is None or markup_amount <= 0:
        return None

    result = []
    base_split = False
    for entry in tagged:
        if not base_split and entry.get("charge_type") == "base":
            reduced = float(entry.get("amount") or 0) - float(markup_amount)
            result.append({**entry, "amount": round(reduced, 2)})
            base_split = True
        else:
            result.append(entry)

    if not base_split:
        return None

    result.append(
        {
            "name": f"Platform Margin ({active_plan})" if active_plan else "Platform Margin",
            "amount": round(float(markup_amount), 2),
            "currency": currency,
            "id": markup_id,
            "charge_type": "platform_fee",
            **({"metadata": {"plan": active_plan}} if active_plan else {}),
        }
    )
    return result


def carrier_cost_from_charges(extra_charges: typing.Iterable[dict]) -> float:
    """Sum of carrier-side charges (base + surcharge + tax) in the typed shape."""
    return round(
        sum(float(c.get("amount") or 0) for c in extra_charges if c.get("charge_type") in CARRIER_CHARGE_TYPES),
        2,
    )


def base_cost_from_charges(extra_charges: typing.Iterable[dict]) -> float:
    """Sum of base charges only (no surcharges, no tax) in the typed shape."""
    return round(
        sum(float(c.get("amount") or 0) for c in extra_charges if c.get("charge_type") == "base"),
        2,
    )


def margin_from_charges(extra_charges: typing.Iterable[dict]) -> float:
    """Sum of merchant-side margin charges (markup + platform_fee)."""
    return round(
        sum(float(c.get("amount") or 0) for c in extra_charges if c.get("charge_type") in MARGIN_CHARGE_TYPES),
        2,
    )


#: Internal rate-meta keys we never want surfaced on merchant responses.
#: `plan_costs` / `plan_cost_types` — even after scrubbing to the active
#: tier, they still reveal the tenant's own markup id and amount.
#: `plan_cost_<slug>` / `plan_rate_<slug>` — flat CSV-import keys for
#: the active tier. `plan` — stamps the tenant's tier onto every rate.
#: `rate_source` — admin-side marker stamped by `Rates.resolve` ("static")
#: that hints at the carrier sourcing path. `actual_rate` — reserved for
#: carrier-actual amounts captured alongside sheet-driven rates (COGS
#: reconciliation channel); admin-only.
#:
#: Admin responses bypass `strip_internal_meta` (e.g. via the admin
#: GraphQL surface), so the stored shape is unchanged.
_INTERNAL_META_EXACT = frozenset(
    {
        "plan_costs",
        "plan_cost_types",
        "plan_rates",
        "plan_rate_types",
        "plan",
        "rate_source",
        "actual_rate",
    }
)
_INTERNAL_META_PREFIXES = ("plan_cost_", "plan_rate_")


def strip_internal_meta(meta: dict | None) -> dict | None:
    """Return a copy of ``meta`` with internal plan/margin keys removed.

    Merchant-facing responses go through this to close SHIP2-1125
    (HIGH): after the hook's cross-tier scrub runs, the surviving active
    tier's `plan_costs[mkp_id]` still exposes the merchant's own markup
    id and amount — which is internal data they shouldn't see on every
    rate response. Admin / billing / fee-capture surfaces bypass this
    helper and see the full meta.

    Input is never mutated. `None` passes through unchanged so callers
    that distinguish missing-meta from empty-meta keep their shape.
    """
    if meta is None:
        return None
    if not isinstance(meta, dict):
        return meta
    result = dict(meta)
    for key in list(result):
        if key in _INTERNAL_META_EXACT:
            result.pop(key, None)
            continue
        if key.startswith(_INTERNAL_META_PREFIXES):
            result.pop(key, None)
    return result


def fold_platform_fees_for_display(extra_charges: list[dict]) -> list[dict]:
    """Merchant-facing view of extra_charges.

    Strips charge_type="platform_fee" entries (our hidden margin) and
    folds their amounts back into the existing Base Charge entry so the
    visible breakdown still sums to total_charge. This preserves the
    pre-typed-breakdown customer UX exactly while keeping the raw stored
    shape available to billing/admin consumers.

    Never mutates the input. Returns a new list of dicts.
    """
    if not extra_charges:
        return []

    platform_fee_total = 0.0
    kept: list[dict] = []
    for entry in extra_charges:
        amount = float(entry.get("amount") or 0)
        if entry.get("charge_type") == "platform_fee":
            platform_fee_total += amount
            continue
        kept.append(dict(entry))

    if platform_fee_total <= 0 or not kept:
        return kept

    for entry in kept:
        if entry.get("charge_type") in ("base", None) and (entry.get("name") or "").strip().lower() in (
            "base charge",
            "base_charge",
        ):
            entry["amount"] = round(float(entry.get("amount") or 0) + platform_fee_total, 2)
            return kept

    # No Base Charge line to fold into — prepend one so the breakdown
    # still sums correctly. Currency inherited from the first entry.
    currency = kept[0].get("currency") if kept else None
    kept.insert(
        0,
        {
            "name": "Base Charge",
            "amount": round(platform_fee_total, 2),
            "currency": currency,
            "charge_type": "base",
        },
    )
    return kept
