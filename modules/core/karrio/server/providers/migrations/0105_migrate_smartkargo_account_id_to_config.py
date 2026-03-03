"""Migrate SmartKargo account_id from credentials to config.primary_id.

This migration moves the account_id field from CarrierConnection.credentials
to CarrierConnection.config.primary_id for all smartkargo connections.
"""

from django.db import migrations


def migrate_account_id_to_config(apps, schema_editor):
    """Migrate account_id from credentials to config.primary_id."""
    CarrierConnection = apps.get_model("providers", "CarrierConnection")

    carriers = CarrierConnection.objects.filter(carrier_code="smartkargo")

    for carrier in carriers:
        credentials = carrier.credentials or {}
        account_id = credentials.pop("account_id", None)

        if account_id:
            config = carrier.config or {}
            config["primary_id"] = account_id
            carrier.config = config
            carrier.credentials = credentials
            carrier.save(update_fields=["config", "credentials"])


def reverse_migration(apps, schema_editor):
    """Reverse: move primary_id back to credentials.account_id."""
    CarrierConnection = apps.get_model("providers", "CarrierConnection")

    carriers = CarrierConnection.objects.filter(carrier_code="smartkargo")

    for carrier in carriers:
        config = carrier.config or {}
        account_id = config.pop("primary_id", None)

        if account_id:
            credentials = carrier.credentials or {}
            credentials["account_id"] = account_id
            carrier.credentials = credentials
            carrier.config = config
            carrier.save(update_fields=["config", "credentials"])


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0104_merge_0103"),
    ]

    operations = [
        migrations.RunPython(
            migrate_account_id_to_config,
            reverse_migration,
        ),
    ]
