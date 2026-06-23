# Data migration: Retroactively snapshot rate-cell essentials and the
# shipping_method {id, name} dict onto shipment.meta for shipments
# purchased before the snapshot writer (manager/serializers/shipment.py:
# build_purchase_snapshot) landed.
#
# Why backfill:
# - The admin shipment list and billing now read `meta.shipping_method.name`
#   to display the composed method name (e.g. "DHL KleinPaket 0 - 1kg").
#   Legacy shipments don't have that key so they fall back to a bare service
#   code. The dict shape also unifies with what the brokered serializer
#   writes going forward.
# - `meta.rate_cell` carries the applied rate cell essentials (rate_id,
#   base_rate, cost, currency, min/max weight, transit_days) so margin
#   recalculations and invoice audits don't have to walk `selected_rate`
#   for every shipment.
#
# Name resolution walks a wide fallback chain so legacy shipments still
# converge to a readable {id, name} dict:
#   1. AccountShippingMethod lookup (by id, if it still exists)
#   2. selected_rate.display_name ("DHL KleinPaket 0 - 1kg")
#   3. service_name + matched weight tier → recomposed display name
#      (mirrors rate_resolver._build_display_name)
#   4. bare service_name ("DHL Paket")
#
# What is NOT backfilled:
# - `plan_at_purchase` — we have no historical record of which plan tier the
#   org was on at label time. Using the current plan would be misleading
#   for shipments purchased months ago.
#
# Idempotent: re-running skips shipments that already have rate_cell, and
# only touches shipping_method entries that lack a real name.
#
# Reverse: removes rate_cell (the only fully-new key). shipping_method
# enrichment is forward-compatible and stays in place.

import logging
import re

from django.db import migrations

logger = logging.getLogger(__name__)

CHUNK = 500
_WEIGHT_SUFFIX_RE = re.compile(r"\d+\s*(?:kg|g|lb)\b", re.IGNORECASE)


def _format_weight(value, decimals=False):
    """Mirror karrio.server.shipping.services.rate_resolver._format_weight."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if decimals or v < 1:
        if v < 0.01:
            return "0"
        if v < 1:
            return f"{v:.2f}".rstrip("0").rstrip(".")
    return f"{int(v)}"


def _compose_display_name(service_name, min_w, max_w):
    """Reconstruct rate_resolver._build_display_name from whatever pieces
    survived on the legacy rate row. Returns bare service_name if no weight
    tier is available."""
    if not service_name:
        return None
    if _WEIGHT_SUFFIX_RE.search(service_name):
        return service_name
    if min_w is None and max_w is None:
        return service_name
    lo_decimals = max_w is not None and float(max_w) < 1
    lo = _format_weight(min_w or 0, decimals=lo_decimals)
    if max_w is None:
        return f"{service_name} {lo}kg+"
    hi = _format_weight(max_w, decimals=lo_decimals)
    return f"{service_name} {lo} - {hi}kg"


def _resolve_fallback_name(meta, selected_rate, rate_meta):
    """Pick the best available name for a shipping_method snapshot."""
    return (
        selected_rate.get("display_name")
        or _compose_display_name(
            rate_meta.get("service_name"),
            rate_meta.get("matched_min_weight"),
            rate_meta.get("matched_max_weight"),
        )
        or rate_meta.get("service_name")
        or meta.get("service_name")
    )


def _coerce_shipping_method(value, method_lookup, fallback_name):
    """Normalize legacy shipping_method shapes to {id, name}.

    Inputs we may see on legacy shipments:
    - dict {id, name}: already structured. If name is empty, hydrate from
      the lookup or the fallback chain so admin/billing aren't stuck with
      a null name (the bug that triggered this migration's second pass).
    - flat string id: expand to {id, name} via lookup, then fallback chain.
    - missing / anything else: synthesize {id: None, name: fallback_name}
      so the admin UI shows the composed display name instead of falling
      all the way through to a bare service code.
    """
    if isinstance(value, dict) and "id" in value:
        existing_name = value.get("name")
        name = existing_name or method_lookup.get(value.get("id")) or fallback_name
        return {"id": value.get("id"), "name": name}

    if isinstance(value, str) and value:
        return {
            "id": value,
            "name": method_lookup.get(value) or fallback_name,
        }

    if fallback_name:
        return {"id": None, "name": fallback_name}

    return None


def _build_rate_cell(selected_rate):
    """Extract rate cell essentials from a stored selected_rate dict.

    Mirrors build_purchase_snapshot() in serializers/shipment.py but is
    duplicated here so the migration is hermetic and won't break if the
    runtime helper signature changes later."""
    rate = selected_rate or {}
    rate_meta = rate.get("meta") or {}
    # Stored rates use `extra_charges` (DRF Rate serializer field); live
    # ShippingMethodRate.to_dict emits `charges` with charge_type tags.
    charges = rate.get("charges") or rate.get("extra_charges") or []
    base_charge = next(
        (
            c
            for c in charges
            if isinstance(c, dict)
            and (
                c.get("charge_type") == "base" or (c.get("name") or "").strip().lower() in {"base charge", "base rate"}
            )
        ),
        None,
    )

    cell: dict = {}
    if rate.get("id"):
        cell["rate_id"] = rate["id"]
    if base_charge and base_charge.get("amount") is not None:
        cell["base_rate"] = base_charge["amount"]
    if rate.get("cost") is not None:
        cell["cost"] = rate["cost"]
    if rate.get("currency"):
        cell["currency"] = rate["currency"]
    if rate_meta.get("matched_min_weight") is not None:
        cell["min_weight"] = rate_meta["matched_min_weight"]
    if rate_meta.get("matched_max_weight") is not None:
        cell["max_weight"] = rate_meta["matched_max_weight"]
    if rate.get("transit_days") is not None:
        cell["transit_days"] = rate["transit_days"]

    return cell


def backfill_purchase_snapshot(apps, schema_editor):
    Shipment = apps.get_model("manager", "Shipment")

    # Optional: AccountShippingMethod lives in the shipping extension module.
    # If the module isn't installed (vanilla karrio) we still backfill
    # rate_cell — we just skip the id → name expansion.
    try:
        AccountShippingMethod = apps.get_model("shipping", "AccountShippingMethod")
        method_lookup = dict(AccountShippingMethod.objects.values_list("id", "name"))
    except LookupError:
        method_lookup = {}

    # Only shipments that completed a purchase have a populated selected_rate
    # JSONField. Filter out drafts; the JSONField equality check works
    # cross-DB without needing the Postgres `has_key` lookup.
    qs = Shipment.objects.exclude(selected_rate={}).exclude(selected_rate=None)

    pending = []
    scanned = 0
    updated = 0
    cells_written = 0
    methods_written = 0

    for shipment in qs.iterator(chunk_size=CHUNK):
        scanned += 1
        meta = dict(shipment.meta or {})
        selected_rate = shipment.selected_rate or {}
        rate_meta = selected_rate.get("meta") or {}

        rate_cell = _build_rate_cell(selected_rate)
        fallback_name = _resolve_fallback_name(meta, selected_rate, rate_meta)
        new_method = _coerce_shipping_method(
            meta.get("shipping_method") or rate_meta.get("shipping_method"),
            method_lookup,
            fallback_name,
        )

        changed = False

        if rate_cell and "rate_cell" not in meta:
            meta["rate_cell"] = rate_cell
            cells_written += 1
            changed = True

        if new_method and meta.get("shipping_method") != new_method:
            meta["shipping_method"] = new_method
            methods_written += 1
            changed = True

        # service_name is heavily used by the admin list as a fallback.
        # Copy it across only when missing so we don't overwrite anything
        # a downstream hook might have populated.
        if "service_name" not in meta and rate_meta.get("service_name"):
            meta["service_name"] = rate_meta["service_name"]
            changed = True

        if changed:
            shipment.meta = meta
            pending.append(shipment)

        if len(pending) >= CHUNK:
            Shipment.objects.bulk_update(pending, ["meta"])
            updated += len(pending)
            pending = []

    if pending:
        Shipment.objects.bulk_update(pending, ["meta"])
        updated += len(pending)

    if scanned:
        logger.info(
            "Backfilled purchase snapshot: scanned=%s updated=%s rate_cell=%s shipping_method=%s",
            scanned,
            updated,
            cells_written,
            methods_written,
        )


def reverse_backfill(apps, schema_editor):
    """Undo only the rate_cell addition. The shipping_method dict shape is
    forward-compatible (consumers that only read `.id` still work) and the
    service_name copy is non-destructive, so neither is removed here."""
    Shipment = apps.get_model("manager", "Shipment")

    pending = []
    cleared = 0

    qs = Shipment.objects.exclude(meta={}).exclude(meta=None)
    for shipment in qs.iterator(chunk_size=CHUNK):
        meta = shipment.meta or {}
        if "rate_cell" not in meta:
            continue
        new_meta = {k: v for k, v in meta.items() if k != "rate_cell"}
        shipment.meta = new_meta
        pending.append(shipment)

        if len(pending) >= CHUNK:
            Shipment.objects.bulk_update(pending, ["meta"])
            cleared += len(pending)
            pending = []

    if pending:
        Shipment.objects.bulk_update(pending, ["meta"])
        cleared += len(pending)

    if cleared:
        logger.info("Cleared rate_cell from meta on %s shipments", cleared)


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0090_redact_persisted_rate_meta"),
    ]

    operations = [
        migrations.RunPython(backfill_purchase_snapshot, reverse_backfill),
    ]
