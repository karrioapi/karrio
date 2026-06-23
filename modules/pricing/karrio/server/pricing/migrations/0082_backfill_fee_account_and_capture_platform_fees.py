"""
Migration: Backfill Fee.account_id and retroactively capture missing
platform_fee Fee rows.

Why this migration exists
─────────────────────────
Two production bugs left historical Fee data incomplete:

1. **NULL account_id**. `capture_fees_for_shipment` was called from the
   shipment post_save signal — which fires on the very first
   `Shipment.objects.create()` call, BEFORE `@owned_model_serializer`'s
   `link_org` writes the ShipmentLink row. `shipment.org.first()` returned
   `None` at that moment, so Fee rows were persisted with
   `account_id=NULL`. The admin Merchants page (and every
   `total_addons_charges` aggregate) filters by `account_id=<org_id>` and
   silently dropped those rows from every total.

2. **No capture for invisible plan markups**. Before the typed charge
   breakdown landed, `capture_fees_for_shipment` identified margin
   entries by `id.startswith("mkp_","chrg_")` in `extra_charges`. Plan
   markups (is_visible=False) were folded into the `Base Charge` line
   with `id=None`, so they never matched. No Fee row was ever written.
   The admin `total_addons_charges` for those shipments was 0 as a
   result.

Both bugs are fixed on the forward path (`fix(pricing): defer fee
capture until org link is written` and the typed-charge-breakdown work).
This migration heals the historical data so existing deployments line
up with the new behaviour.

Safety
──────
- Idempotent. Skips any (shipment_id, markup_id) pair that already has
  a Fee row. Only touches Fee rows whose `account_id` is NULL or empty.
- Read-only against `Shipment` / `ShipmentLink` / `Organization` /
  `Markup` — only writes to the `Fee` table.
- Irreversible. The reverse step raises a `RuntimeError` per
  `.claude/rules/ci-patterns.md` — un-populating account_id would be
  destructive and un-disambiguable from legitimately NULL rows.
"""

from django.db import migrations
from django.db.models import Q

# Max rows per bulk_update / bulk_create batch. Small enough to keep memory
# flat on prod-sized datasets, large enough to amortise round-trips.
BATCH = 500


def _backfill_account_id(Fee, ShipmentLink):
    """Populate account_id on Fee rows orphaned by the pre-fix signal race."""
    qs = Fee.objects.filter(Q(account_id__isnull=True) | Q(account_id=""))
    shipment_ids = list(qs.values_list("shipment_id", flat=True).distinct())
    if not shipment_ids:
        return 0
    link_map = dict(ShipmentLink.objects.filter(item_id__in=shipment_ids).values_list("item_id", "org_id"))
    updates = []
    for fee in qs.iterator(chunk_size=BATCH):
        org_id = link_map.get(fee.shipment_id)
        if org_id and fee.account_id != org_id:
            fee.account_id = org_id
            updates.append(fee)
    if updates:
        Fee.objects.bulk_update(updates, ["account_id"], batch_size=BATCH)
    return len(updates)


def _capture_missing_platform_fees(Fee, Shipment, Markup, Organization, ShipmentLink):
    """Create Fee rows for shipments whose platform_fees were never captured.

    Uses `charge_breakdown.normalize_extra_charges` to reconstruct the typed
    breakdown from historical `selected_rate` shapes (folded and non-folded).
    That helper is a pure function (no migration-state-sensitive imports),
    so it is safe to call from a data migration.
    """
    # Lazy import — the helper ships with the same PR as this migration.
    from karrio.server.pricing.charge_breakdown import MARGIN_CHARGE_TYPES, normalize_extra_charges

    # Index existing Fee rows by (shipment_id, markup_id) for idempotent skips.
    existing_pairs = set(
        Fee.objects.exclude(markup_id__isnull=True).exclude(markup_id="").values_list("shipment_id", "markup_id")
    )
    link_map = dict(ShipmentLink.objects.values_list("item_id", "org_id"))
    org_plan_map = {}
    for org in Organization.objects.all().only("id", "metadata").iterator(chunk_size=200):
        org_plan_map[org.id] = (org.metadata or {}).get("plan") or "start"
    markups_by_id = {m.id: m for m in Markup.objects.all().only("id", "markup_type", "amount", "meta")}

    to_create = []
    qs = (
        Shipment.objects.exclude(selected_rate__isnull=True)
        .exclude(status="draft")
        .only("id", "selected_rate", "test_mode", "status")
    )
    for shipment in qs.iterator(chunk_size=200):
        sr = shipment.selected_rate or {}
        if not sr:
            continue
        meta = sr.get("meta") or {}

        # Fast-reject: only bother if there's a plan-cost signal we can act
        # on. Keeps the loop O(1) for non-brokered shipments.
        has_plan_signal = bool(
            meta.get("plan_costs")
            or meta.get("plan")
            or any(k.startswith("plan_cost_") or k.startswith("plan_rate_") for k in meta)
        )
        if not has_plan_signal:
            continue

        org_id = link_map.get(shipment.id)
        if not org_id:
            continue  # orphan — cannot attribute to an account.

        org_plan = org_plan_map.get(org_id) or "start"
        typed = normalize_extra_charges(sr, org_plan=org_plan)
        currency = sr.get("currency") or "USD"
        carrier_code = meta.get("carrier_code") or sr.get("carrier_name") or ""
        service_code = sr.get("service") or ""
        connection_id = meta.get("carrier_connection_id") or meta.get("connection_id") or ""

        for charge in typed:
            if charge.get("charge_type") not in MARGIN_CHARGE_TYPES:
                continue
            markup_id = charge.get("id")
            if not markup_id:
                continue
            if (shipment.id, markup_id) in existing_pairs:
                continue
            existing_pairs.add((shipment.id, markup_id))
            markup = markups_by_id.get(markup_id)
            to_create.append(
                Fee(
                    shipment_id=shipment.id,
                    markup_id=markup_id,
                    account_id=org_id,
                    test_mode=shipment.test_mode,
                    name=charge.get("name", ""),
                    amount=charge.get("amount", 0) or 0,
                    currency=currency,
                    fee_type=(markup.markup_type if markup else "AMOUNT"),
                    percentage=(markup.amount if markup and markup.markup_type == "PERCENTAGE" else None),
                    carrier_code=carrier_code,
                    service_code=service_code,
                    connection_id=connection_id,
                )
            )
    if to_create:
        Fee.objects.bulk_create(to_create, batch_size=BATCH)
    return len(to_create)


def forward(apps, schema_editor):
    Fee = apps.get_model("pricing", "Fee")
    Markup = apps.get_model("pricing", "Markup")

    # orgs is the enterprise package — single-org deployments don't install
    # it, so model lookup must be defensive (mirrors migration 0079).
    try:
        ShipmentLink = apps.get_model("orgs", "ShipmentLink")
        Organization = apps.get_model("orgs", "Organization")
        Shipment = apps.get_model("manager", "Shipment")
    except LookupError:
        return

    updated = _backfill_account_id(Fee, ShipmentLink)
    created = _capture_missing_platform_fees(Fee, Shipment, Markup, Organization, ShipmentLink)
    if updated or created:
        # Visible in migration output so ops can confirm the backfill ran.
        # noqa: T201 — migrations print directly (see 0077 for precedent).
        print(  # noqa: T201
            f"[pricing.0082] account_id backfilled on {updated} Fee row(s); "
            f"captured {created} missing platform_fee Fee row(s)"
        )


def reverse(apps, schema_editor):
    raise RuntimeError(
        "Migration 0082_backfill_fee_account_and_capture_platform_fees is not "
        "reversible. Populated account_ids cannot be un-populated without "
        "losing the distinction between migration-written and pre-existing "
        "NULL values, and the synthesised Fee rows have no canonical marker "
        "to retract them. Roll forward only."
    )


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0081_alter_markup_meta"),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
