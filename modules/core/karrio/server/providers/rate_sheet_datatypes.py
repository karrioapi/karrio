"""Typed dataclasses for rate sheet JSONField payloads.

Canonical shape for every well-known dict that rides inside
`RateSheet.service_rates`, `.zones`, `.surcharges`, `.pricing_config`, and
`ServiceLevel.metadata`. Consumers convert at the storage boundary:

    # in:  dict -> typed
    row = lib.to_object(ServiceRateRow, rate_dict)

    # out: typed -> dict (for JSONField storage or JSON response)
    payload = row.to_dict()

Follows the pattern in `modules/support/karrio/server/support/datatypes.py`.
Storage shape is unchanged — these types describe the dict, they do not
replace it on disk.
"""

from __future__ import annotations

import attr
import karrio.lib as lib

# Plan slugs are intentionally NOT a fixed tuple — plan tiers can be renamed
# or added (scale, growth, etc.) without code changes. The importer discovers
# slugs dynamically from CSV column names (plan_cost_<slug>/plan_rate_<slug>)
# and matches them against active Markup rows with `meta.plan == slug`.


@attr.s(auto_attribs=True)
class PlanOverride:
    """Per-rate custom-margin override, keyed by markup_id.

    Written by:
        * rate sheet CSV import (`plan_cost_<slug>` columns)
        * Edit Service Rate dialog (Plans → Custom Margin section)

    Read by:
        * `karrio.server.pricing.models.Markup.apply_charge`
        * `modules.shipping.services.rate_resolver._apply_markups_to_rates`
    """

    plan_costs: dict = attr.Factory(dict)  # {markup_id: amount}
    plan_cost_types: dict = attr.Factory(dict)  # {markup_id: "AMOUNT"|"PERCENTAGE"}

    def override_for(self, markup_id: str) -> tuple:
        """Return (amount, type) for a markup, or (None, None) if no override."""
        return self.plan_costs.get(markup_id), self.plan_cost_types.get(markup_id)

    def is_empty(self) -> bool:
        return not self.plan_costs

    @classmethod
    def from_dict(cls, data) -> PlanOverride:
        """Construct from a (possibly partial) dict. Accepts None."""
        if not data:
            return cls()
        return cls(
            plan_costs=dict(data.get("plan_costs") or {}),
            plan_cost_types=dict(data.get("plan_cost_types") or {}),
        )

    def to_dict(self) -> dict:
        """Canonical serialize via `lib.to_dict(attr.asdict(self))`."""
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class RateRowMeta:
    """Per-service-rate row meta. Rides on each `service_rates` list item.

    Surcharge and plan_rate fields are informational (rendered by the CSV
    preview grid). `plan_override` is authoritative — consumed by the markup
    applier at rate-fetch time. `excluded_markup_ids` disables markups for
    this specific rate row.
    """

    # Surcharges (informational)
    fuel_surcharge: float | None = None
    seasonal_surcharge: float | None = None
    customs_surcharge: float | None = None
    energy_surcharge: float | None = None
    road_toll: float | None = None
    security_surcharge: float | None = None

    # Per-rate plan override (authoritative, supersedes markup.amount).
    # plan_rate_<slug> / plan_cost_<slug> values from CSV imports land here
    # via PlanOverride, keyed by the matched markup_id; the raw slug values
    # also land in `extras` for preview-only display.
    plan_override: PlanOverride = attr.Factory(PlanOverride)

    signature: bool | None = None
    transit_time: str | None = None
    notes: str | None = None

    # Rate-level markup / surcharge exclusions (UI-driven).
    excluded_markup_ids: list = attr.Factory(list)
    excluded_surcharge_ids: list = attr.Factory(list)

    # Generic extras bag: any additional keys (age_check, saturday,
    # unresolved plan_rate_<slug>/plan_cost_<slug> values, carrier-specific
    # flags, etc.) survive round-trip without schema changes.
    extras: dict = attr.Factory(dict)

    _STRUCTURED_KEYS = (
        "fuel_surcharge",
        "seasonal_surcharge",
        "customs_surcharge",
        "energy_surcharge",
        "road_toll",
        "security_surcharge",
        "signature",
        "transit_time",
        "notes",
        "excluded_markup_ids",
        "excluded_surcharge_ids",
        "plan_costs",
        "plan_cost_types",
    )

    @classmethod
    def from_dict(cls, data) -> RateRowMeta:
        """Construct from a storage dict (accepts None)."""
        if not data:
            return cls()
        extras = {k: v for k, v in data.items() if k not in cls._STRUCTURED_KEYS}
        return cls(
            fuel_surcharge=data.get("fuel_surcharge"),
            seasonal_surcharge=data.get("seasonal_surcharge"),
            customs_surcharge=data.get("customs_surcharge"),
            energy_surcharge=data.get("energy_surcharge"),
            road_toll=data.get("road_toll"),
            security_surcharge=data.get("security_surcharge"),
            plan_override=PlanOverride.from_dict(data),
            signature=data.get("signature"),
            transit_time=data.get("transit_time"),
            notes=data.get("notes"),
            excluded_markup_ids=list(data.get("excluded_markup_ids") or []),
            excluded_surcharge_ids=list(data.get("excluded_surcharge_ids") or []),
            extras=extras,
        )

    def to_dict(self) -> dict:
        """Serialize to the flat storage shape.

        `lib.to_dict(attr.asdict(self))` gets us clean (None-stripped) keys;
        we then lift `plan_override.*` and `extras.*` to the top level so
        downstream consumers (UI preview, universal rating proxy) see the
        same flat keys they always have.
        """
        out = lib.to_dict(attr.asdict(self))
        out.pop("plan_override", None)
        if not self.plan_override.is_empty():
            out["plan_costs"] = dict(self.plan_override.plan_costs)
            out["plan_cost_types"] = dict(self.plan_override.plan_cost_types)
        out.update(out.pop("extras", None) or {})
        return out


@attr.s(auto_attribs=True)
class ServiceRateRow:
    """One row in `rate_sheet.service_rates` (JSONField)."""

    service_id: str = ""
    zone_id: str = ""
    rate: float | None = None
    cost: float | None = None
    min_weight: float | None = None
    max_weight: float | None = None
    shipment_type: str = "outbound"
    transit_days: object = None  # str|int|None (preserve original shape)
    meta: RateRowMeta = attr.Factory(RateRowMeta)
    plan_rate_start: float | None = None
    plan_cost_start: float | None = None
    plan_rate_advanced: float | None = None
    plan_cost_advanced: float | None = None
    plan_rate_pro: float | None = None
    plan_cost_pro: float | None = None
    plan_rate_enterprise: float | None = None
    plan_cost_enterprise: float | None = None
    surcharge_ids: list = attr.Factory(list)

    @classmethod
    def from_dict(cls, data) -> ServiceRateRow:
        if not data:
            return cls()
        return cls(
            service_id=data.get("service_id", "") or "",
            zone_id=data.get("zone_id", "") or "",
            rate=data.get("rate"),
            cost=data.get("cost"),
            min_weight=data.get("min_weight"),
            max_weight=data.get("max_weight"),
            shipment_type=data.get("shipment_type", "outbound") or "outbound",
            transit_days=data.get("transit_days"),
            meta=RateRowMeta.from_dict(data.get("meta")),
            plan_rate_start=data.get("plan_rate_start"),
            plan_cost_start=data.get("plan_cost_start"),
            plan_rate_advanced=data.get("plan_rate_advanced"),
            plan_cost_advanced=data.get("plan_cost_advanced"),
            plan_rate_pro=data.get("plan_rate_pro"),
            plan_cost_pro=data.get("plan_cost_pro"),
            plan_rate_enterprise=data.get("plan_rate_enterprise"),
            plan_cost_enterprise=data.get("plan_cost_enterprise"),
            surcharge_ids=list(data.get("surcharge_ids") or []),
        )

    def to_dict(self) -> dict:
        """Serialize via `lib.to_dict(attr.asdict(self))`, then substitute
        the nested `meta` with its own flattened dict."""
        out = lib.to_dict(attr.asdict(self))
        meta_dict = self.meta.to_dict()
        if meta_dict:
            out["meta"] = meta_dict
        else:
            out.pop("meta", None)
        return out


@attr.s(auto_attribs=True)
class ZoneDef:
    """One item in `rate_sheet.zones` (JSONField)."""

    id: str = ""
    label: str = ""
    country_codes: list = attr.Factory(list)
    postal_codes: list = attr.Factory(list)
    cities: list = attr.Factory(list)
    transit_days: object = None
    transit_time: str | None = None
    rate: float | None = None
    min_weight: float | None = None
    max_weight: float | None = None
    weight_unit: str | None = None
    meta: dict = attr.Factory(dict)

    @classmethod
    def from_dict(cls, data) -> ZoneDef:
        if not data:
            return cls()
        return cls(
            id=data.get("id", "") or "",
            label=data.get("label", "") or "",
            country_codes=list(data.get("country_codes") or []),
            postal_codes=list(data.get("postal_codes") or []),
            cities=list(data.get("cities") or []),
            transit_days=data.get("transit_days"),
            transit_time=data.get("transit_time"),
            rate=data.get("rate"),
            min_weight=data.get("min_weight"),
            max_weight=data.get("max_weight"),
            weight_unit=data.get("weight_unit"),
            meta=dict(data.get("meta") or {}),
        )

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class SurchargeDef:
    """One item in `rate_sheet.surcharges` (JSONField)."""

    id: str = ""
    name: str = ""
    amount: float = 0.0
    surcharge_type: str = "AMOUNT"
    cost: float | None = None
    active: bool = True

    @classmethod
    def from_dict(cls, data) -> SurchargeDef:
        if not data:
            return cls()
        return cls(
            id=data.get("id", "") or "",
            name=data.get("name", "") or "",
            amount=float(data.get("amount") or 0.0),
            surcharge_type=data.get("surcharge_type", "AMOUNT") or "AMOUNT",
            cost=data.get("cost"),
            active=bool(data.get("active", True)),
        )

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))


@attr.s(auto_attribs=True)
class ServiceMetadata:
    """`ServiceLevel.metadata` shape.

    `shipping_method` — display name override returned in rate responses
    instead of `service.service_name` when set (see PR #444).
    """

    shipping_method: str | None = None
    extras: dict = attr.Factory(dict)

    _STRUCTURED_KEYS = ("shipping_method",)

    @classmethod
    def from_dict(cls, data) -> ServiceMetadata:
        if not data:
            return cls()
        extras = {k: v for k, v in data.items() if k not in cls._STRUCTURED_KEYS}
        return cls(shipping_method=data.get("shipping_method"), extras=extras)

    def to_dict(self) -> dict:
        """Serialize via `lib.to_dict(attr.asdict(self))`, lifting extras
        to the top level so callers see a flat dict."""
        out = lib.to_dict(attr.asdict(self))
        out.update(out.pop("extras", None) or {})
        return out


@attr.s(auto_attribs=True)
class RateSheetPricingConfig:
    """`rate_sheet.pricing_config` shape."""

    excluded_markup_ids: list = attr.Factory(list)
    sort_order: int | None = None

    @classmethod
    def from_dict(cls, data) -> RateSheetPricingConfig:
        if not data:
            return cls()
        return cls(
            excluded_markup_ids=list(data.get("excluded_markup_ids") or []),
            sort_order=data.get("sort_order"),
        )

    def to_dict(self) -> dict:
        return lib.to_dict(attr.asdict(self))
