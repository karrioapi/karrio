# Data migration: Populate carrier JSONField from FK relationships

import logging

from django.db import migrations

logger = logging.getLogger("karrio.server")

# Stream rows in bounded chunks and write them back with bulk_update so the
# migration never loads an entire table into memory or issues one UPDATE per row
# (GH #1123). Each table is processed independently and is idempotent: rows whose
# snapshot is already populated are skipped, so re-running is a no-op.
BATCH_SIZE = 2000


def get_carrier_name(carrier):
    """Get carrier name from carrier code."""
    from karrio.core.utils import DP

    try:
        return DP.to_dict(carrier.data).get("carrier_name", carrier.carrier_code)
    except Exception:
        return carrier.carrier_code


def create_carrier_snapshot(carrier):
    """Create carrier snapshot dict from Carrier model instance."""
    if carrier is None:
        return None

    return {
        "connection_id": carrier.id,
        "connection_type": "account",  # All existing carriers are account connections
        "carrier_code": carrier.carrier_code,
        "carrier_id": carrier.carrier_id,
        "carrier_name": get_carrier_name(carrier),
        "test_mode": carrier.test_mode,
    }


def _populate_from_fk(Model, fk_field, label):
    """Copy a carrier FK snapshot into the ``carrier`` JSONField in bounded batches.

    Streams only rows that still need a snapshot (FK set, carrier empty) via a
    server-side cursor, and writes them back with bulk_update in fixed-size
    batches. Returns the number of rows updated.
    """
    queryset = (
        Model.objects.filter(**{f"{fk_field}__isnull": False, "carrier__isnull": True})
        .select_related(fk_field)
        .order_by("pk")
    )

    batch = []
    total = 0

    def flush():
        nonlocal total
        if batch:
            Model.objects.bulk_update(batch, ["carrier"], batch_size=BATCH_SIZE)
            total += len(batch)
            logger.info(f"0078 populate {label}: {total} rows updated")
            batch.clear()

    for instance in queryset.iterator(chunk_size=BATCH_SIZE):
        carrier = getattr(instance, fk_field)
        if carrier and not instance.carrier:
            instance.carrier = create_carrier_snapshot(carrier)
            batch.append(instance)
        if len(batch) >= BATCH_SIZE:
            flush()

    flush()
    return total


def populate_carrier_snapshots(apps, schema_editor):
    """
    Populate carrier JSONField from FK relationships.

    This copies carrier information from:
    - Pickup.pickup_carrier -> Pickup.carrier
    - Tracking.tracking_carrier -> Tracking.carrier
    - DocumentUploadRecord.upload_carrier -> DocumentUploadRecord.carrier
    - Manifest.manifest_carrier -> Manifest.carrier
    - Shipment.selected_rate_carrier -> Shipment.carrier (dedicated field, consistent with other models)

    Production-safe (GH #1123): each table is streamed in chunks and written
    back with bulk_update — no per-row save, no full-table load — and is
    idempotent so it can be re-run safely.
    """
    mappings = [
        ("Pickup", "pickup_carrier"),
        ("Tracking", "tracking_carrier"),
        ("DocumentUploadRecord", "upload_carrier"),
        ("Manifest", "manifest_carrier"),
        ("Shipment", "selected_rate_carrier"),
    ]

    for model_name, fk_field in mappings:
        Model = apps.get_model("manager", model_name)
        _populate_from_fk(Model, fk_field, model_name)


def reverse_migration(apps, schema_editor):
    """
    Reverse migration: Clear carrier JSONField (data preserved in FKs).

    Note: The FK data is still preserved, so this is safe to reverse.
    """
    Pickup = apps.get_model("manager", "Pickup")
    Tracking = apps.get_model("manager", "Tracking")
    DocumentUploadRecord = apps.get_model("manager", "DocumentUploadRecord")
    Manifest = apps.get_model("manager", "Manifest")
    Shipment = apps.get_model("manager", "Shipment")

    Pickup.objects.update(carrier=None)
    Tracking.objects.update(carrier=None)
    DocumentUploadRecord.objects.update(carrier=None)
    Manifest.objects.update(carrier=None)
    Shipment.objects.update(carrier=None)


class Migration(migrations.Migration):
    """
    Step 2: Data migration - Populate carrier snapshots from FK relationships.

    This migration copies carrier information from FK fields to the new JSONField.
    The FK fields are still preserved at this point.
    """

    dependencies = [
        ("manager", "0077_add_carrier_snapshot_fields"),
    ]

    operations = [
        migrations.RunPython(populate_carrier_snapshots, reverse_migration),
    ]
