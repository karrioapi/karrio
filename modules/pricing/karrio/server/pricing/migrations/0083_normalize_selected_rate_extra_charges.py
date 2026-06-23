"""
Migration: Normalize Shipment.selected_rate.extra_charges + canonicalize
the platform-margin display name across historical shipments.

Why this migration exists
─────────────────────────
Three production bugs converged to break the admin "Cost" column on
new shipments after the Fee → Margin label rename:

1. **`Markup.apply_charge` wrote `markup.name` directly** into the rate
   breakdown (`extra_charges[].name`). Renaming the markup row therefore
   rewrote the line item on every new shipment, coupling merchant-facing
   line items to admin labels. The admin app filters Cost by
   `name.includes('platform fee')` — once the label said "Platform
   Margin" (typo'd as "Marin"), the filter missed every new row.

2. **`normalize_extra_charges` synthesized a duplicate `platform_fee`**
   when a rate had its margin entry already typed (from the post-
   processing hook) but its carrier-side entries (Base Charge, Road
   Toll, …) untyped. `_is_typed()` requires *all* entries typed, so the
   adapter fell through and appended a second platform_fee on top of
   the existing one — double-counting margin and breaking
   `sum(extras) == total_charge`.

3. **Markup row name typo**. The Start-tier markup
   (`mkp_49d4b43379ef405b9adb29b5c63eb676`) was renamed to
   "Shipping Start - Platform Marin" — missing the trailing 'g'.
   Cosmetic for the admin Markups page, but it leaked into stored
   `extra_charges` because of bug #1.

The forward fixes change `Markup.apply_charge` to emit a stable
`Platform Margin (<plan>)` synthetic name and harden
`normalize_extra_charges` to detect an existing platform_fee. This
migration heals historical shipment data so older shipments render the
same way as new ones in the admin Cost column.

What this migration does
────────────────────────
1. **Markup table**. Fix `Markup.name` rows where the value ends with
   "Marin" (typo, missing 'g') so the admin Markups page renders
   correctly going forward.

2. **Shipment.selected_rate.extra_charges**. For every Shipment with
   `selected_rate`:
     - Tag every `extra_charges` entry with the right `charge_type`
       (base | surcharge | markup | platform_fee) using the same
       `_tag_carrier_entries` heuristic as the runtime adapter.
     - Dedupe duplicate `platform_fee` entries (same markup id),
       keeping the first occurrence.
     - Canonicalize plan-scoped `platform_fee` entry names to
       "Platform Margin (<plan>)" — including any "Marin" typos.
     - Trust `selected_rate.total_charge` (cash already moved); only
       adjust the platform_fee `amount` if the breakdown diverges,
       never touch `total_charge`.

3. **Fee table — backfill**. Walk every shipment again and write any
   missing `Fee` rows for charges with charge_type ∈ {markup,
   platform_fee} that have a recoverable markup id and a linked org.
   Real-time capture has been silently dropping fees because the
   duplicate-platform_fee bug surfaced a unique-constraint violation
   on the second insert; this restores the dropped rows.

4. **Fee table — name canonicalization**. Rewrite every `Fee.name`
   value to match the canonical `selected_rate.extra_charges` name so
   the admin Charges page and reporting aggregates show one label per
   semantic fee instead of a mix of historical strings ("Platform Fee
   (start)", "Shipping Start - Platform Marin").

Safety
──────
- Idempotent: re-running over already-typed/canonicalized data is a
  no-op (the canonicalizer overwrites with the same value).
- Read-mostly: only writes shipments where `selected_rate` actually
  changed shape.
- Bounded memory via `iterator(chunk_size=BATCH)` and `bulk_update`.
- Reversible: the reverse step is a no-op (the typed shape is a strict
  superset of the legacy shape — leaving it in place doesn't break the
  legacy code paths).
"""

from __future__ import annotations

import copy
import logging

from django.db import migrations

logger = logging.getLogger(__name__)

BATCH = 500
CARRIER_CHARGE_TYPES = ("base", "surcharge", "tax")
MARGIN_CHARGE_TYPES = ("markup", "platform_fee")


def _tag_carrier_entries(extra_charges: list[dict]) -> list[dict]:
    """Mirrors charge_breakdown._tag_carrier_entries, inlined for migration safety."""
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


def _dedupe_platform_fees(extra_charges: list[dict]) -> tuple[list[dict], bool]:
    """Drop duplicate platform_fee rows for the same markup id.

    Returns (deduped_list, changed_flag).
    """
    seen_ids: set[str] = set()
    seen_unidentified = False
    result: list[dict] = []
    changed = False
    for entry in extra_charges:
        if entry.get("charge_type") != "platform_fee":
            result.append(entry)
            continue
        eid = entry.get("id")
        if eid:
            if eid in seen_ids:
                changed = True
                continue
            seen_ids.add(eid)
        else:
            # Keep at most one un-identified platform_fee row.
            if seen_unidentified:
                changed = True
                continue
            seen_unidentified = True
        result.append(entry)
    return result, changed


def _canonicalize_margin_names(extra_charges: list[dict]) -> tuple[list[dict], bool]:
    """Rewrite plan-scoped platform_fee names to 'Platform Margin (<plan>)'."""
    result = []
    changed = False
    for entry in extra_charges:
        if entry.get("charge_type") != "platform_fee":
            result.append(entry)
            continue
        plan = (entry.get("metadata") or {}).get("plan")
        canonical = f"Platform Margin ({plan})" if plan else "Platform Margin"
        if entry.get("name") != canonical:
            changed = True
        new_entry = dict(entry)
        new_entry["name"] = canonical
        result.append(new_entry)
    return result, changed


def _reconcile_margin_amount(extra_charges: list[dict], total_charge: float) -> tuple[list[dict], bool]:
    """Adjust the platform_fee amount so sum(extras) == total_charge.

    `total_charge` is authoritative — it is the price actually charged.
    When the deduped breakdown no longer reconciles (because we removed
    a duplicate amount), re-allocate the missing/extra delta onto the
    surviving platform_fee entry. If no platform_fee exists or there is
    no delta, the breakdown is left untouched.
    """
    extras_sum = round(sum(float(c.get("amount") or 0) for c in extra_charges), 2)
    delta = round(total_charge - extras_sum, 2)
    if abs(delta) < 0.005:
        return extra_charges, False

    # Prefer a plan-scoped platform_fee, fall back to any platform_fee.
    target_idx = None
    for idx, entry in enumerate(extra_charges):
        if entry.get("charge_type") == "platform_fee":
            target_idx = idx
            if (entry.get("metadata") or {}).get("plan"):
                break

    if target_idx is None:
        return extra_charges, False

    new_entry = dict(extra_charges[target_idx])
    new_entry["amount"] = round(float(new_entry.get("amount") or 0) + delta, 2)
    result = list(extra_charges)
    result[target_idx] = new_entry
    return result, True


def _normalize(selected_rate: dict) -> tuple[dict, bool]:
    """Return (new_selected_rate, changed)."""
    if not isinstance(selected_rate, dict):
        return selected_rate, False
    extras = list(selected_rate.get("extra_charges") or [])
    if not extras:
        return selected_rate, False

    original = copy.deepcopy(extras)
    tagged = _tag_carrier_entries(extras)
    deduped, dedupe_changed = _dedupe_platform_fees(tagged)
    canonical, name_changed = _canonicalize_margin_names(deduped)

    total_charge = float(selected_rate.get("total_charge") or 0)
    reconciled, amount_changed = _reconcile_margin_amount(canonical, total_charge)

    changed = original != reconciled or dedupe_changed or name_changed or amount_changed
    if not changed:
        return selected_rate, False

    new_rate = dict(selected_rate)
    new_rate["extra_charges"] = reconciled
    return new_rate, True


def _normalize_shipments(apps, schema_editor):
    Shipment = apps.get_model("manager", "Shipment")
    qs = Shipment.objects.exclude(selected_rate__isnull=True).exclude(selected_rate={})
    pending: list = []
    touched = 0
    for shipment in qs.only("id", "selected_rate").iterator(chunk_size=BATCH):
        new_rate, changed = _normalize(shipment.selected_rate)
        if not changed:
            continue
        shipment.selected_rate = new_rate
        pending.append(shipment)
        if len(pending) >= BATCH:
            Shipment.objects.bulk_update(pending, ["selected_rate"])
            touched += len(pending)
            pending = []
    if pending:
        Shipment.objects.bulk_update(pending, ["selected_rate"])
        touched += len(pending)
    logger.info("[0083] Normalized selected_rate.extra_charges on %d shipments", touched)


def _fix_markup_typo(apps, schema_editor):
    Markup = apps.get_model("pricing", "Markup")
    pending = []
    for markup in Markup.objects.iterator(chunk_size=BATCH):
        name = markup.name or ""
        # Match the trailing 'Marin' typo without touching legitimate
        # words like 'Marinade' or hypothetical 'Marina'. The admin label
        # always ends with 'Margin', so we only correct values where
        # 'Marin' appears at end-of-string.
        if name.endswith("Marin"):
            markup.name = name[:-5] + "Margin"
            pending.append(markup)
        elif " Marin " in name:
            markup.name = name.replace(" Marin ", " Margin ")
            pending.append(markup)
    if pending:
        Markup.objects.bulk_update(pending, ["name"])
    logger.info("[0083] Fixed 'Marin' typo on %d Markup rows", len(pending))


def _canonical_fee_name(fee, markup_meta_by_id):
    """Mirror the canonical synthesis used on selected_rate.extra_charges.

    Plan-scoped fees normalize to "Platform Margin (<plan>)". Visible
    non-plan fees keep the (typo-corrected) admin label since those are
    real merchant-facing line items with intentional names (e.g.
    "Coverage - 100").
    """
    plan = (markup_meta_by_id.get(fee.markup_id) or {}).get("plan") if fee.markup_id else None
    if plan:
        return f"Platform Margin ({plan})"
    name = fee.name or ""
    if name.endswith("Marin"):
        return name[:-5] + "Margin"
    if " Marin " in name:
        return name.replace(" Marin ", " Margin ")
    return name


def _canonicalize_fee_names(apps, schema_editor):
    """Rewrite Fee.name on existing rows to match the canonical
    selected_rate.extra_charges name. Without this the admin Charges
    page and reporting aggregates show a mix of historical labels
    ("Platform Fee (start)", "Shipping Start - Platform Marin") for
    semantically identical fee rows."""
    Fee = apps.get_model("pricing", "Fee")
    Markup = apps.get_model("pricing", "Markup")

    markup_meta_by_id = dict(Markup.objects.values_list("id", "meta"))

    pending = []
    for fee in Fee.objects.iterator(chunk_size=BATCH):
        new_name = _canonical_fee_name(fee, markup_meta_by_id)
        if new_name and new_name != fee.name:
            fee.name = new_name
            pending.append(fee)
            if len(pending) >= BATCH:
                Fee.objects.bulk_update(pending, ["name"])
                pending = []
    if pending:
        Fee.objects.bulk_update(pending, ["name"])
    logger.info("[0083] Canonicalized %d Fee.name rows", len(pending))


def _backfill_missing_fees(apps, schema_editor):
    """Backfill Fee rows for shipments where real-time capture was
    silently dropped by the duplicate-platform_fee bug.

    Only writes a Fee for charges with charge_type ∈ {markup,
    platform_fee}, a recoverable markup id, and a linked org. Idempotent
    against (shipment_id, markup_id).
    """
    Shipment = apps.get_model("manager", "Shipment")
    ShipmentLink = apps.get_model("orgs", "ShipmentLink")
    Fee = apps.get_model("pricing", "Fee")
    Markup = apps.get_model("pricing", "Markup")

    org_by_shipment = dict(ShipmentLink.objects.values_list("item_id", "org_id"))
    markup_by_id = {m.id: m for m in Markup.objects.all()}

    qs = Shipment.objects.exclude(selected_rate__isnull=True).exclude(selected_rate={})
    new_rows = []
    seen_pairs: set = set()
    existing_pairs = set(Fee.objects.values_list("shipment_id", "markup_id"))

    for shipment in qs.only("id", "selected_rate", "test_mode").iterator(chunk_size=BATCH):
        sr = shipment.selected_rate or {}
        extras = sr.get("extra_charges") or []
        meta = sr.get("meta") or {}
        carrier_code = meta.get("carrier_code") or sr.get("carrier_name", "")
        service_code = sr.get("service", "")
        connection_id = meta.get("carrier_connection_id", "") or meta.get("connection_id", "")
        currency = sr.get("currency", "EUR")
        account_id = org_by_shipment.get(shipment.id)
        if not account_id:
            continue

        for charge in extras:
            ct = charge.get("charge_type")
            if ct not in MARGIN_CHARGE_TYPES:
                continue
            charge_id = charge.get("id")
            if not charge_id:
                continue
            pair = (shipment.id, charge_id)
            if pair in existing_pairs or pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            markup = markup_by_id.get(charge_id)
            new_rows.append(
                Fee(
                    shipment_id=shipment.id,
                    markup_id=charge_id,
                    account_id=account_id,
                    test_mode=getattr(shipment, "test_mode", False),
                    name=charge.get("name", ""),
                    amount=charge.get("amount", 0),
                    currency=currency,
                    fee_type=getattr(markup, "markup_type", None) or "AMOUNT",
                    percentage=(
                        getattr(markup, "amount", None)
                        if markup and getattr(markup, "markup_type", None) == "PERCENTAGE"
                        else None
                    ),
                    carrier_code=carrier_code,
                    service_code=service_code,
                    connection_id=connection_id,
                )
            )
            if len(new_rows) >= BATCH:
                Fee.objects.bulk_create(new_rows, ignore_conflicts=True)
                new_rows = []

    if new_rows:
        Fee.objects.bulk_create(new_rows, ignore_conflicts=True)
    logger.info(
        "[0083] Backfilled %d Fee rows for shipments missed by real-time capture",
        len(seen_pairs),
    )


def forwards(apps, schema_editor):
    _fix_markup_typo(apps, schema_editor)
    _normalize_shipments(apps, schema_editor)
    # Order matters: backfill new Fee rows BEFORE renaming existing ones,
    # so the new rows already use the canonical name (they inherit it
    # from the just-normalized selected_rate.extra_charges).
    _backfill_missing_fees(apps, schema_editor)
    _canonicalize_fee_names(apps, schema_editor)


def backwards(apps, schema_editor):
    # Forward path is a strict shape upgrade — re-typed and renamed
    # entries remain compatible with all legacy readers. There is no
    # safe way to "un-canonicalize" because the original arbitrary
    # admin labels are not recoverable. Leave the normalized shape in
    # place rather than corrupting data on rollback.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0082_backfill_fee_account_and_capture_platform_fees"),
        ("manager", "0089_rename_purchased_to_created_and_remove_choices"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
