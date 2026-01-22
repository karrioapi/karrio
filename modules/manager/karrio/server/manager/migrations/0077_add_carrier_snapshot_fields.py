# Add carrier JSONField to models before data migration

import functools
import karrio.server.core.utils as utils
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Step 1: Add carrier JSONField to Pickup, Tracking, DocumentUploadRecord, Manifest, Shipment.
    Also adds carrier_ids JSONField to Shipment.

    This migration adds the new carrier snapshot fields but does NOT remove the old FK fields yet.
    The old FK fields are needed by the data migration (0078) to populate the carrier snapshots.
    """

    dependencies = [
        ("manager", "0076_remove_customs_model"),
    ]

    operations = [
        # Add carrier field to Pickup
        migrations.AddField(
            model_name="pickup",
            name="carrier",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Carrier snapshot at time of pickup creation",
            ),
        ),
        # Add carrier field to Tracking
        migrations.AddField(
            model_name="tracking",
            name="carrier",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Carrier snapshot at time of tracker creation",
            ),
        ),
        # Add carrier field to DocumentUploadRecord
        migrations.AddField(
            model_name="documentuploadrecord",
            name="carrier",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Carrier snapshot at time of document upload",
            ),
        ),
        # Add carrier field to Manifest
        migrations.AddField(
            model_name="manifest",
            name="carrier",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Carrier snapshot at time of manifest creation",
            ),
        ),
        # Add carrier field to Shipment (consistent with other models)
        migrations.AddField(
            model_name="shipment",
            name="carrier",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Carrier snapshot at time of label purchase",
            ),
        ),
        # Add carrier_ids field to Shipment
        migrations.AddField(
            model_name="shipment",
            name="carrier_ids",
            field=models.JSONField(
                blank=True,
                null=True,
                default=functools.partial(utils.identity, value=[]),
                help_text="List of carrier IDs to filter rate requests",
            ),
        ),
    ]
