# Cleanup migration: Remove is_system and active_users from Carrier after data migration

import django.db.models.deletion
import functools
import karrio.server.core.fields
import karrio.server.core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Step 3: Remove legacy fields from Carrier model.

    This migration removes:
    - is_system field (system carriers are now in SystemConnection)
    - active_users M2M (user access is now via BrokeredConnection)

    Also updates meta options and field definitions.
    """

    dependencies = [
        ("providers", "0093_migrate_system_carriers_data"),
    ]

    operations = [
        # Remove legacy fields
        migrations.RemoveField(
            model_name="carrier",
            name="active_users",
        ),
        migrations.RemoveField(
            model_name="carrier",
            name="is_system",
        ),
        # Update meta options
        migrations.AlterModelOptions(
            name="carrier",
            options={
                "ordering": ["test_mode", "-created_at"],
                "verbose_name": "Carrier Connection",
                "verbose_name_plural": "Carrier Connections",
            },
        ),
        # Update field definitions to match new model
        migrations.AlterField(
            model_name="carrier",
            name="active",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Enable/disable carrier connection",
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="capabilities",
            field=karrio.server.core.fields.MultiChoiceField(
                choices=[
                    ("pickup", "pickup"),
                    ("rating", "rating"),
                    ("shipping", "shipping"),
                    ("tracking", "tracking"),
                    ("paperless", "paperless"),
                    ("manifest", "manifest"),
                    ("duties", "duties"),
                    ("insurance", "insurance"),
                    ("webhook", "webhook"),
                    ("oauth", "oauth"),
                ],
                default=functools.partial(
                    karrio.server.core.models._identity, *(), **{"value": []}
                ),
                help_text="Enabled carrier capabilities",
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="carrier_code",
            field=models.CharField(
                db_index=True,
                default="generic",
                help_text="Carrier identifier (e.g., 'dhl_express', 'fedex')",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="carrier_id",
            field=models.CharField(
                db_index=True,
                help_text="User-defined connection identifier",
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="credentials",
            field=models.JSONField(
                default=functools.partial(
                    karrio.server.core.models._identity, *(), **{"value": {}}
                ),
                help_text="Carrier API credentials",
            ),
        ),
        migrations.AlterField(
            model_name="carrier",
            name="rate_sheet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="carrier_connections",
                to="providers.ratesheet",
            ),
        ),
        # Add index for common queries
        migrations.AddIndex(
            model_name="carrier",
            index=models.Index(
                fields=["carrier_code", "active"], name="carrier_carrier_275509_idx"
            ),
        ),
        # Rename table to 'carrier' (may already be this name)
        migrations.AlterModelTable(
            name="carrier",
            table="carrier",
        ),
    ]
