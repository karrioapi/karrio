# Cleanup migration: Remove carrier FK/M2M fields after data migration

from django.db import migrations


class Migration(migrations.Migration):
    """
    Step 3: Remove carrier FK/M2M fields after data has been migrated to JSONField.

    This migration removes:
    - Pickup.pickup_carrier (FK)
    - Tracking.tracking_carrier (FK)
    - DocumentUploadRecord.upload_carrier (FK)
    - Manifest.manifest_carrier (FK)
    - Shipment.selected_rate_carrier (FK)
    - Shipment.carriers (M2M)

    All carrier data is now stored in JSONField carrier snapshots.
    """

    dependencies = [
        ("manager", "0078_populate_carrier_snapshots"),
    ]

    operations = [
        # Remove Pickup.pickup_carrier FK
        migrations.RemoveField(
            model_name="pickup",
            name="pickup_carrier",
        ),
        # Remove Tracking.tracking_carrier FK
        migrations.RemoveField(
            model_name="tracking",
            name="tracking_carrier",
        ),
        # Remove DocumentUploadRecord.upload_carrier FK
        migrations.RemoveField(
            model_name="documentuploadrecord",
            name="upload_carrier",
        ),
        # Remove Manifest.manifest_carrier FK
        migrations.RemoveField(
            model_name="manifest",
            name="manifest_carrier",
        ),
        # Remove Shipment.selected_rate_carrier FK
        migrations.RemoveField(
            model_name="shipment",
            name="selected_rate_carrier",
        ),
        # Remove Shipment.carriers M2M
        migrations.RemoveField(
            model_name="shipment",
            name="carriers",
        ),
    ]
