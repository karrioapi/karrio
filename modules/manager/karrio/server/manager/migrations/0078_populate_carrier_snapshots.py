# Data migration: Populate carrier JSONField from FK relationships

from django.db import migrations


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


def populate_carrier_snapshots(apps, schema_editor):
    """
    Populate carrier JSONField from FK relationships.

    This copies carrier information from:
    - Pickup.pickup_carrier -> Pickup.carrier
    - Tracking.tracking_carrier -> Tracking.carrier
    - DocumentUploadRecord.upload_carrier -> DocumentUploadRecord.carrier
    - Manifest.manifest_carrier -> Manifest.carrier
    - Shipment.selected_rate_carrier -> Shipment.carrier (dedicated field, consistent with other models)
    """
    Pickup = apps.get_model("manager", "Pickup")
    Tracking = apps.get_model("manager", "Tracking")
    DocumentUploadRecord = apps.get_model("manager", "DocumentUploadRecord")
    Manifest = apps.get_model("manager", "Manifest")
    Shipment = apps.get_model("manager", "Shipment")

    # Populate Pickup.carrier from pickup_carrier FK
    for pickup in Pickup.objects.select_related("pickup_carrier").all():
        if pickup.pickup_carrier and not pickup.carrier:
            pickup.carrier = create_carrier_snapshot(pickup.pickup_carrier)
            pickup.save(update_fields=["carrier"])

    # Populate Tracking.carrier from tracking_carrier FK
    for tracking in Tracking.objects.select_related("tracking_carrier").all():
        if tracking.tracking_carrier and not tracking.carrier:
            tracking.carrier = create_carrier_snapshot(tracking.tracking_carrier)
            tracking.save(update_fields=["carrier"])

    # Populate DocumentUploadRecord.carrier from upload_carrier FK
    for record in DocumentUploadRecord.objects.select_related("upload_carrier").all():
        if record.upload_carrier and not record.carrier:
            record.carrier = create_carrier_snapshot(record.upload_carrier)
            record.save(update_fields=["carrier"])

    # Populate Manifest.carrier from manifest_carrier FK
    for manifest in Manifest.objects.select_related("manifest_carrier").all():
        if manifest.manifest_carrier and not manifest.carrier:
            manifest.carrier = create_carrier_snapshot(manifest.manifest_carrier)
            manifest.save(update_fields=["carrier"])

    # Populate Shipment.carrier from selected_rate_carrier FK (consistent with other models)
    for shipment in Shipment.objects.select_related("selected_rate_carrier").all():
        if shipment.selected_rate_carrier and not shipment.carrier:
            shipment.carrier = create_carrier_snapshot(shipment.selected_rate_carrier)
            shipment.save(update_fields=["carrier"])


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
