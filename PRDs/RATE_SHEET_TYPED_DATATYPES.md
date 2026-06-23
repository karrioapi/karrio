# PRD — Rate Sheet Typed Datatypes

**Status:** Draft · 2026-04-13
**Author:** Daniel K
**Scope:** `karrio/modules/data`, `karrio/modules/pricing`, `modules/shipping`
**Stacks on:** `feat/shipping-method-name-and-plan-override-import` (#444)

---

## Summary

Rate sheet data flows through ~155 call sites as **loose dicts** today:
`service_rates = [{"service_id": ..., "zone_id": ..., "rate": ..., "meta": {"plan_costs": {...}}}]`.
The importer, rate resolver, pricing module, and preview UI all do
`.get("field")` lookups with no compile-time shape safety. A typo like
`"plan_cost"` (missing `s`) silently returns `None` and the override never
fires — which is how the plan-cost override bug in #444 hid for this long.

Introduce `@attr.s(auto_attribs=True)` dataclasses for every well-known rate
sheet JSON shape, converting at the ORM boundary with `lib.to_object(T, dict)`
and `attr.asdict(obj)`. Follow the pattern used by
`modules/support/karrio/server/support/datatypes.py` and
`modules/wawi/karrio/server/wawi/datatypes.py`.

## Non-goals

- **Django JSONField shape does not change.** Storage stays as dict (for
  backward compat with existing rows and the frontend CSV preview).
- **No REST / GraphQL schema changes.** Serializers already emit dicts.
- **No frontend TypeScript changes.** Types are for Python consumers only.
- **Not refactoring every call site.** Focus on hot paths; peripheral sites
  can migrate incrementally as they're touched.

## Existing datatype patterns to follow

- `modules/support/karrio/server/support/datatypes.py` — 44 lines, 5 classes.
  Uses `@attr.s(auto_attribs=True)`, `lib.to_dict(attr.asdict(self))` for
  output. Simple + clean.
- `modules/wawi/karrio/server/wawi/datatypes.py` — 135 lines, shows nested
  composition with `Optional[T]` fields.
- `karrio.core.models.RateDetails` etc. — karrio SDK dataclasses, reference
  for `JList[T]` / `JStruct[T]` usage for nested lists.

## Type Inventory

| New Type | Replaces dict shape | Lives in |
|---|---|---|
| `PlanOverride` | `{plan_costs: {mid: float}, plan_cost_types: {mid: str}}` | `rate_sheet_datatypes.py` |
| `RateRowMeta` | Per-row meta dict from `_build_rate_meta` | `rate_sheet_datatypes.py` |
| `ServiceRateRow` | Item in `rate_sheet.service_rates` | `rate_sheet_datatypes.py` |
| `ZoneDef` | Item in `rate_sheet.zones` | `rate_sheet_datatypes.py` |
| `SurchargeDef` | Item in `rate_sheet.surcharges` | `rate_sheet_datatypes.py` |
| `ServiceMetadata` | `ServiceLevel.metadata` (`shipping_method`, etc.) | `rate_sheet_datatypes.py` |
| `RateSheetPricingConfig` | `rate_sheet.pricing_config` (`excluded_markup_ids`, `sort_order`) | `rate_sheet_datatypes.py` |

Canonical location: new file `karrio/modules/core/karrio/server/providers/rate_sheet_datatypes.py` so both `karrio.server.data` (importer) and `karrio.server.shipping` (resolver) consume the same types.

### Contracts

```python
@attr.s(auto_attribs=True)
class PlanOverride:
    """Per-rate custom-margin override, keyed by markup_id.

    Written by:  rate sheet CSV import (plan_cost_<slug> columns),
                 Edit Service Rate dialog (Plans → Custom Margin section)
    Read by:     pricing.models.Markup.apply_charge
                 shipping.services.rate_resolver._apply_markups_to_rates
                 ui/components/service-rate-editor-dialog.tsx
    """
    plan_costs: dict[str, float] = attr.Factory(dict)        # {markup_id: amount}
    plan_cost_types: dict[str, str] = attr.Factory(dict)     # {markup_id: "AMOUNT"|"PERCENTAGE"}

    def override_for(self, markup_id: str) -> tuple[float | None, str | None]:
        """Return (amount, type) for a markup, or (None, None) if no override."""
        return self.plan_costs.get(markup_id), self.plan_cost_types.get(markup_id)

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class RateRowMeta:
    """Per-service-rate row meta. Rides on each service_rates list item.

    Surcharge amounts are informational (used by the CSV preview grid to
    render columns). Plan override is authoritative — consumed by the
    markup applier at rate-fetch time.
    """
    # Surcharges (informational; per-row amounts shown in CSV preview)
    fuel_surcharge: float | None = None
    seasonal_surcharge: float | None = None
    customs_surcharge: float | None = None
    energy_surcharge: float | None = None
    road_toll: float | None = None
    security_surcharge: float | None = None

    # Plan rates (informational)
    plan_rate_start: float | None = None
    plan_rate_advanced: float | None = None
    plan_rate_pro: float | None = None
    plan_rate_enterprise: float | None = None

    # Plan override (authoritative, supersedes markup.amount)
    plan_override: PlanOverride = attr.Factory(PlanOverride)

    # Explicit signature / transit fields (nullable)
    signature: bool | None = None
    transit_time: str | None = None

    # Excluded markups (rate-level exclusions ride here)
    excluded_markup_ids: list[str] = attr.Factory(list)

    # Carrier-specific feature flags / unknown extras
    extras: dict = attr.Factory(dict)

    def to_dict(self) -> dict:
        """Serialize to the storage shape (flat dict). Flattens plan_override."""
        d = lib.to_dict(attr.asdict(self))
        # Pull plan_override fields up to top-level for storage parity
        override = d.pop("plan_override", None) or {}
        if override.get("plan_costs"):
            d["plan_costs"] = override["plan_costs"]
        if override.get("plan_cost_types"):
            d["plan_cost_types"] = override["plan_cost_types"]
        # Merge extras into top-level
        d.update(d.pop("extras", None) or {})
        return d


@attr.s(auto_attribs=True)
class ServiceRateRow:
    """One row in rate_sheet.service_rates (JSONField)."""
    service_id: str = ""
    zone_id: str = ""
    rate: float | None = None
    cost: float | None = None
    min_weight: float | None = None
    max_weight: float | None = None
    shipment_type: str = "outbound"
    transit_days: str | int | None = None
    meta: RateRowMeta = attr.Factory(RateRowMeta)
    # Informational mirrors (kept out-of-meta for UI convenience)
    plan_rate_start: float | None = None
    plan_cost_start: float | None = None
    plan_rate_advanced: float | None = None
    plan_cost_advanced: float | None = None
    plan_rate_pro: float | None = None
    plan_cost_pro: float | None = None
    plan_rate_enterprise: float | None = None
    plan_cost_enterprise: float | None = None
    surcharge_ids: list[str] = attr.Factory(list)

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class ZoneDef:
    id: str = ""
    label: str = ""
    country_codes: list[str] = attr.Factory(list)
    postal_codes: list[str] = attr.Factory(list)
    cities: list[str] = attr.Factory(list)
    transit_days: str | int | None = None
    transit_time: str | None = None
    rate: float | None = None
    min_weight: float | None = None
    max_weight: float | None = None
    weight_unit: str | None = None
    meta: dict = attr.Factory(dict)

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class SurchargeDef:
    id: str = ""
    name: str = ""
    amount: float = 0.0
    surcharge_type: str = "AMOUNT"
    cost: float | None = None
    active: bool = True

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class ServiceMetadata:
    shipping_method: str | None = None
    extras: dict = attr.Factory(dict)

    def to_dict(self) -> dict:
        d = lib.to_dict(attr.asdict(self))
        d.update(d.pop("extras", None) or {})
        return d


@attr.s(auto_attribs=True)
class RateSheetPricingConfig:
    excluded_markup_ids: list[str] = attr.Factory(list)
    sort_order: int | None = None

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))
```

## Call Sites to Refactor (hot path)

| File | Change |
|---|---|
| `karrio/modules/data/.../rate_sheets.py` — `_build_rate_meta` | Return `RateRowMeta` (existing callers get `.to_dict()` at storage boundary) |
| Same — `build_rate_sheet_input_from_flat` | Emit `ServiceRateRow`/`ZoneDef`/`SurchargeDef` instances, flatten with `.to_dict()` before returning |
| `modules/shipping/.../rate_resolver.py` — `_resolve_rate_for_service` | Convert `best_rate_data` → `ServiceRateRow` once; read `.meta.plan_override` typed |
| Same — `_apply_markups_to_rates` | Read `rate.meta["plan_costs"]` via `PlanOverride(...).override_for(markup.id)` |
| `karrio/modules/pricing/.../models.py` — `Markup.apply_charge` | Same override lookup via typed `PlanOverride` |

## Call Sites NOT Refactored (deferred)

- `SystemRateSheet.service_rates` JSONField storage — still dict for DB/frontend compat.
- Admin GraphQL mutations (`update_service_rate`, `batch_update_service_rates`) — continue to accept/emit dicts; can adopt types later.
- CSV preview TSX — TypeScript-side typing is a separate project.
- The universal SDK `rating_proxy.py` — operates at karrio Rate layer, outside this module boundary.

## Tests

No new tests — the refactor must be **behavior-preserving**. Green light:
- `./bin/run-server-tests` passes (hundreds of existing tests cover the hot path).
- `karrio.server.data.tests.test_rate_sheet_import` — 35 tests (importer).
- `karrio.server.shipping.tests.test_plan_based_pricing` — 12 tests (resolver + override application).
- `karrio.server.pricing.tests` — markup apply_charge path.

Plus two new targeted tests asserting the typed helpers work:
- `test_rate_row_meta_round_trips_through_to_dict`
- `test_plan_override_override_for_returns_tuple`

## Rollout

1. Merge PR #444 first (this work builds on it).
2. Land this refactor as an isolated PR that strictly preserves behavior — no functional changes, just typing.
3. Future PRs migrate remaining dict sites as they're touched.

## Architecture

```
       CSV / API / UI (dict shape)
                │
                ▼
   ┌────────────────────────────────┐
   │ lib.to_object(T, dict)          │   ← boundary-in
   │ = typed dataclass               │
   └──────────────┬─────────────────┘
                  │
                  ▼  (typed code)
     rate_resolver, apply_charge,
     importer, signals
                  │
                  ▼
   ┌────────────────────────────────┐
   │ obj.to_dict() / attr.asdict    │   ← boundary-out
   │ = dict shape                    │
   └──────────────┬─────────────────┘
                  ▼
       Django JSONField / response
```
