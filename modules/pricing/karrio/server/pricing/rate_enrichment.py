"""Brokered live-carrier rate enrichment.

Bridges the gap between the two `Rates.*` paths:

  - `Rates.resolve` (rate-sheet resolver) emits rates whose `meta` already
    carries `plan_costs` / `plan_cost_<slug>` from the matched sheet row.
  - `Rates.fetch` (live carrier API → `<carrier>.parse_rate_response`) emits
    rates with carrier-side meta only — no plan_costs.

Without enrichment, `Markup.apply_charge` on the second path can't find the
per-row override and falls through to `Markup.amount` (= 0.0 by design on
plan-tier markups). This module copies the rate sheet's plan keys onto the
rate's meta in place, leaving carrier-side `total_charge` / `extra_charges`
untouched. The markup applier then adds the correct platform_fee line.
"""

from __future__ import annotations

import typing

import attr
import karrio.lib as lib
from karrio.core import models as core_models
from karrio.server.core import datatypes
from karrio.server.providers.rate_sheet_datatypes import (
    ServiceRateRow,
    ZoneDef,
)
from karrio.server.providers.service_level_matching import pick_best_service_level

# Flat per-tier keys are CSV-import shape (`plan_cost_start`, ...). Plan
# slugs are intentionally open-ended at the system level; we drive the
# enumeration off `ServiceRateRow`'s typed fields rather than re-listing.
_FLAT_KEY_PREFIX: typing.Final = "plan_cost_"


@attr.s(auto_attribs=True)
class _RouteInfo:
    """Subset of a rate-fetch payload needed to match a sheet row.

    The carrier API gave us a rate for a specific (recipient, parcels)
    request; we re-derive only what's needed to look up the corresponding
    rate-sheet row: destination country (zone selector) and billable
    weight (band selector).
    """

    country_code: str = ""
    weight_kg: float = 0.0

    @classmethod
    def from_payload(cls, payload: dict | None) -> _RouteInfo:
        if not isinstance(payload, dict):
            return cls()
        recipient = payload.get("recipient") or {}
        parcels = [
            lib.to_object(core_models.Parcel, raw) for raw in (payload.get("parcels") or []) if isinstance(raw, dict)
        ]
        weight_kg = float(lib.to_packages(parcels).weight.KG or 0.0) if parcels else 0.0
        return cls(
            country_code=(recipient.get("country_code") or "").upper(),
            weight_kg=round(weight_kg, 3),
        )

    @property
    def is_resolvable(self) -> bool:
        """A row match needs both inputs — bail early if either is empty."""
        return bool(self.country_code) and self.weight_kg > 0


def _resolve_zone_id(zones: list[ZoneDef], country_code: str) -> str | None:
    if not zones:
        return None
    if len(zones) == 1:
        return zones[0].id or None
    return next(
        (zone.id for zone in zones if any(code.upper() == country_code for code in zone.country_codes)),
        None,
    )


def _row_matches(
    row: ServiceRateRow,
    *,
    service_id: str,
    zone_id: str | None,
    weight_kg: float,
) -> bool:
    return (
        row.service_id == service_id
        and (zone_id is None or row.zone_id == zone_id)
        and (row.min_weight or 0) <= weight_kg < (row.max_weight or float("inf"))
    )


def _match_rate_sheet_row(
    sheet,
    service_code: str,
    route: _RouteInfo,
    service_name: str | None = None,
) -> ServiceRateRow | None:
    """Pick the tightest-fitting service_rates row for (service, zone, weight).

    When several ServiceLevels share a `service_code` (e.g. UPS Standard to
    Door / Saturday / Return all carry `service_code=ups_standard` because UPS
    only defines one carrier code 11 — saturday is a request option, return is
    a return-service option, etc.), the rate's emitted `meta.service_name`
    uniquely identifies which variant produced the rate. Prefer a service_name
    match over a code-only match so plan_costs from the wrong variant don't
    leak in.
    """
    matching = [svc for svc in sheet.services.all() if svc.service_code == service_code]
    if not matching:
        return None

    # When several variants share `service_code`, prefer the one whose
    # `service_name` matches the rate emission. Falls back to all matches
    # when no service_name is provided (e.g. retro-recalculation paths).
    if service_name:
        picked = pick_best_service_level(matching, service_code, service_name=service_name)
        if picked is not None:
            matching = [picked]

    service_ids = {svc.id for svc in matching}

    zones = [ZoneDef.from_dict(raw) for raw in (getattr(sheet, "zones", None) or [])]
    zone_id = _resolve_zone_id(zones, route.country_code)

    rows = [ServiceRateRow.from_dict(raw) for raw in (getattr(sheet, "service_rates", None) or [])]
    candidates = [
        row
        for row in rows
        if row.service_id in service_ids
        and (zone_id is None or row.zone_id == zone_id)
        and (row.min_weight or 0) <= route.weight_kg < (row.max_weight or float("inf"))
    ]
    return min(candidates, default=None, key=lambda r: r.min_weight or 0)


def plan_keys_for_request(
    sheet,
    service_code: str,
    payload: dict | None,
) -> dict:
    """Public entry point for callers that already have a rate sheet in
    hand and want the plan keys that would be merged onto a rate's meta
    for the given (service, recipient, parcels) request.

    Used by:
      - `enrich_brokered_rates_with_sheet_meta` (booking-time after-hook)
      - `bridge.management.commands.recalculate_shipment_rates`
        `_refresh_platform_fee_only` (retroactive correction)

    Returns an empty dict when the sheet has no row that matches the
    request — caller then leaves the rate's meta untouched and the markup
    applier falls through to `Markup.amount` (matches the live booking
    behavior on the same input).
    """
    if sheet is None:
        return {}
    route = _RouteInfo.from_payload(payload)
    if not route.is_resolvable:
        return {}
    row = _match_rate_sheet_row(sheet, service_code, route)
    if row is None:
        return {}
    return _plan_keys_from_row(row)


def _service_name_from_rate(rate) -> str | None:
    meta = getattr(rate, "meta", None)
    if not isinstance(meta, dict):
        return None
    name = meta.get("service_name")
    if not isinstance(name, str) or not name.strip():
        return None
    return name.strip()


def _is_already_enriched(rate_meta: dict) -> bool:
    """Skip rates whose meta already carries any plan_cost data — the
    resolver path populates them, and that data is authoritative."""
    if rate_meta.get("plan_costs"):
        return True
    return any(isinstance(key, str) and key.startswith(_FLAT_KEY_PREFIX) for key in rate_meta)


def _plan_keys_from_row(row: ServiceRateRow) -> dict:
    """Plan keys to merge into rate.meta.

    Sources, in order:
      - structured `plan_costs` / `plan_cost_types` lifted from
        `RateRowMeta.plan_override` via `PlanOverride.to_dict()` (which
        skips them entirely when empty).
      - flat `plan_cost_<slug>` keys discovered on the typed
        `ServiceRateRow` itself (CSV-import shape).
    """
    structured = row.meta.plan_override.to_dict()
    flat = {
        field.name: getattr(row, field.name)
        for field in attr.fields(ServiceRateRow)
        if field.name.startswith(_FLAT_KEY_PREFIX) and getattr(row, field.name) is not None
    }
    return {**structured, **flat}


def _eligible_rates(rates: typing.Iterable[datatypes.Rate]) -> list[datatypes.Rate]:
    """Rates eligible for enrichment: meta is a dict, has a connection id,
    and isn't already carrying plan_cost data."""
    return [
        rate
        for rate in (rates or [])
        if isinstance(getattr(rate, "meta", None), dict)
        and rate.meta.get("carrier_connection_id")
        and not _is_already_enriched(rate.meta)
    ]


def _sheets_by_connection(
    connection_ids: typing.Iterable[str],
) -> dict[str, typing.Any]:
    """Single batched query — ``SystemConnection.id → SystemRateSheet``.

    Keyed on ``SystemConnection.id`` because ``rate.meta.carrier_connection_id``
    follows the carrier-snapshot convention (system_connection_id for
    brokered rates, matching ``core.utils.create_carrier_snapshot``).
    Connections without a rate sheet are absent from the result.
    """
    ids = list({cid for cid in connection_ids if cid})
    if not ids:
        return {}
    # Lazy import — providers signals load at app-ready, model registries
    # may not be settled at module import time.
    from karrio.server.providers import models as prv

    system = prv.SystemConnection.objects.for_rates().filter(id__in=ids)
    return {sc.id: sc.rate_sheet for sc in system if sc.rate_sheet is not None}


def enrich_brokered_rates_with_sheet_meta(
    result: datatypes.RateResponse,
    payload: dict | None,
) -> None:
    """Mutate `result.rates[*].meta` in place to carry plan_costs from the
    matching rate-sheet row, for any rate whose `carrier_connection_id`
    points at a brokered system connection with a rate sheet.

    Contract — what this DOES and does NOT touch:
      - DOES: copy `plan_costs`, `plan_cost_types`, and flat
        `plan_cost_<slug>` keys from the matched rate-sheet row onto
        `rate.meta`. These keys are inputs to `Markup.apply_charge`, which
        runs immediately after and adds a platform_fee entry to
        `extra_charges` (amount = per-band `plan_cost_<plan>`).
      - DOES NOT: modify `rate.total_charge`, `rate.extra_charges`, or any
        carrier-side meta keys (`carrier_connection_id`, `service_name`,
        `rate_provider`, etc.).

    The carrier's `base + surcharges + tax` as returned by the live Rate
    API stay verbatim — they are what the carrier will bill. We only add
    JTL's platform markup (sourced from the rate sheet, per plan tier and
    weight band) on top. For carriers with a working Rate API the customer
    pays `carrier_total + platform_fee`, with the platform fee coming from
    the rate sheet (not from `Markup.amount`, which is 0.0 by design for
    plan-tier markups — per-row `plan_costs` are authoritative).

    No-op when the request payload (recipient + parcels) is unavailable,
    since we can't determine the matching zone+weight band without it.
    """
    if not getattr(result, "rates", None):
        return

    eligible = _eligible_rates(result.rates)
    if not eligible:
        return

    sheets = _sheets_by_connection(rate.meta["carrier_connection_id"] for rate in eligible)
    if not sheets:
        return

    route = _RouteInfo.from_payload(payload)
    if not route.is_resolvable:
        return

    for rate in eligible:
        sheet = sheets.get(rate.meta["carrier_connection_id"])
        if sheet is None:
            continue
        row = _match_rate_sheet_row(
            sheet,
            rate.service,
            route,
            service_name=_service_name_from_rate(rate),
        )
        if row is None:
            continue
        rate.meta.update(_plan_keys_from_row(row))
