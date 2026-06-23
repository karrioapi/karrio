"""Data migration: redact persisted rate.meta on Shipment rows.

Before this PR, `gateway.Rates.fetch.process_rate` stamped
`carrier_connection_id: carrier.id` onto every rate's meta dict. For
system / brokered connections that raw value is a SystemConnection or
BrokeredConnection PK — security-sensitive. Now the GraphQL/REST
boundary strips it at serialize time, but the underlying JSON blob is
still on disk and would re-leak any time a future code path reads it
without going through the resolver.

This migration scrubs already-persisted blobs:

* For every `Shipment.selected_rate.meta` and each rate in
  `Shipment.rates[*].meta` that points at a SystemConnection or
  BrokeredConnection PK, drop `carrier_connection_id`.
* Always backfill `connection_kind` from the Shipment's `carrier`
  snapshot (`carrier.connection_type`), so the tenant-side redaction
  helper has the discriminator it expects.

Once this has run in production the legacy `decrypt_id_or_passthrough`
acceptance and the raw-id fallback in `resolve_carrier_connection` can
be removed in a follow-up PR.
"""

from django.db import migrations

_SYSTEM_KINDS = {"system", "brokered"}


def _is_system_or_brokered_id(conn_id, system_ids, brokered_ids):
    if not conn_id:
        return False
    return conn_id in system_ids or conn_id in brokered_ids


def _scrub_rate(rate, kind_from_shipment, system_ids, brokered_ids):
    """Return a (possibly-mutated) rate dict; True if anything changed."""
    if not isinstance(rate, dict):
        return rate, False
    meta = rate.get("meta")
    if not isinstance(meta, dict):
        return rate, False

    changed = False
    new_meta = dict(meta)

    if "connection_kind" not in new_meta and kind_from_shipment:
        new_meta["connection_kind"] = kind_from_shipment
        changed = True

    raw_cid = new_meta.get("carrier_connection_id")
    kind = new_meta.get("connection_kind")
    if raw_cid and (kind in _SYSTEM_KINDS or _is_system_or_brokered_id(raw_cid, system_ids, brokered_ids)):
        new_meta.pop("carrier_connection_id", None)
        if "connection_kind" not in new_meta:
            new_meta["connection_kind"] = "system"
        changed = True

    if changed:
        return {**rate, "meta": new_meta}, True
    return rate, False


def redact_persisted_rate_meta(apps, schema_editor):
    Shipment = apps.get_model("manager", "Shipment")

    try:
        SystemConnection = apps.get_model("providers", "SystemConnection")
        BrokeredConnection = apps.get_model("providers", "BrokeredConnection")
    except LookupError:
        # Models not present in this migration state — nothing to scrub.
        return

    system_ids = set(SystemConnection.objects.values_list("id", flat=True))
    brokered_ids = set(BrokeredConnection.objects.values_list("id", flat=True))
    if not system_ids and not brokered_ids:
        return

    updated_shipments = 0
    for shipment in Shipment.objects.only("id", "carrier", "selected_rate", "rates").iterator(chunk_size=500):
        carrier_snapshot = shipment.carrier or {}
        kind_from_shipment = carrier_snapshot.get("connection_type")

        shipment_changed = False

        if isinstance(shipment.selected_rate, dict):
            scrubbed, changed = _scrub_rate(shipment.selected_rate, kind_from_shipment, system_ids, brokered_ids)
            if changed:
                shipment.selected_rate = scrubbed
                shipment_changed = True

        if isinstance(shipment.rates, list) and shipment.rates:
            new_rates = []
            rates_changed = False
            for r in shipment.rates:
                scrubbed, changed = _scrub_rate(r, kind_from_shipment, system_ids, brokered_ids)
                new_rates.append(scrubbed)
                rates_changed = rates_changed or changed
            if rates_changed:
                shipment.rates = new_rates
                shipment_changed = True

        if shipment_changed:
            shipment.save(update_fields=["selected_rate", "rates"])
            updated_shipments += 1

    if updated_shipments:
        import logging

        logging.getLogger("karrio.server.manager.migrations").info(
            "Redacted carrier_connection_id from %d Shipment rate-meta blobs",
            updated_shipments,
        )


def reverse_migration(apps, schema_editor):
    # No-op: the raw PKs were the leak we just removed. Reversing the
    # scrub would re-leak them and we don't keep the audit trail needed
    # to reconstitute the exact pre-migration shape.
    pass


class Migration(migrations.Migration):
    """Strip raw SystemConnection / BrokeredConnection PKs from persisted rate.meta."""

    dependencies = [
        ("manager", "0089_rename_purchased_to_created_and_remove_choices"),
        # We read from providers.SystemConnection / providers.BrokeredConnection.
        # Pin to the latest providers head so both models exist.
        ("providers", "0111_carrier_options_frozen_connection_type"),
    ]

    operations = [
        migrations.RunPython(redact_persisted_rate_meta, reverse_migration),
    ]
