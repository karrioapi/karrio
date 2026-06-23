"""Translate BrokeredConnection PKs in Markup.connection_ids to SystemConnection PKs.

`rate.meta.carrier_connection_id` for brokered rates now records the underlying
SystemConnection PK (per the snapshot convention in
`karrio.server.core.utils.create_carrier_snapshot`). `Markup._is_applicable`
filters by comparing this against `Markup.connection_ids`, so any admin-
configured markups that listed a `BrokeredConnection` PK would silently stop
matching after the snapshot-alignment change.

This migration rewrites `Markup.connection_ids` so each BrokeredConnection PK
is replaced by its `system_connection_id`. SystemConnection and
CarrierConnection PKs pass through unchanged. The result is deduplicated to
collapse cases where both BrokeredConnection.id and SystemConnection.id were
listed for the same upstream system.

Reverse migration is a no-op — we don't keep the mapping needed to restore
which PK a SystemConnection.id was rewritten from.
"""

from django.db import migrations


def translate_connection_ids(apps, schema_editor):
    Markup = apps.get_model("pricing", "Markup")
    try:
        BrokeredConnection = apps.get_model("providers", "BrokeredConnection")
    except LookupError:
        # Providers app missing in this migration state — nothing to do.
        return

    brokered_to_system = dict(BrokeredConnection.objects.values_list("id", "system_connection_id"))
    if not brokered_to_system:
        return

    updated = 0
    for markup in Markup.objects.only("id", "connection_ids").iterator(chunk_size=500):
        ids = markup.connection_ids or []
        if not ids:
            continue

        rewritten = [brokered_to_system.get(cid, cid) for cid in ids]
        # Order-preserving dedup so admins see a stable list when they re-open
        # the markup in the admin.
        deduped = list(dict.fromkeys(rewritten))

        if deduped != ids:
            markup.connection_ids = deduped
            markup.save(update_fields=["connection_ids"])
            updated += 1

    if updated:
        import logging

        logging.getLogger("karrio.server.pricing.migrations").info(
            "Rewrote BrokeredConnection PKs in Markup.connection_ids for %d markup(s)",
            updated,
        )


def reverse_migration(apps, schema_editor):
    # The original mapping (system_connection_id -> brokered_connection.id) was
    # not 1:1 (multiple brokered rows can share a system_connection), so a
    # reverse rewrite isn't well-defined. Leave the data as-is.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "0083_normalize_selected_rate_extra_charges"),
        # Reads providers.BrokeredConnection — pin to its latest head so the
        # model is available when this runs.
        ("providers", "0111_carrier_options_frozen_connection_type"),
    ]

    operations = [
        migrations.RunPython(translate_connection_ids, reverse_migration),
    ]
