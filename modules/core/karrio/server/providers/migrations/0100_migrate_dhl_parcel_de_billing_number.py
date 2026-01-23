"""Migrate DHL Parcel DE billing_number from credentials to config.

This migration moves the billing_number field from CarrierConnection.credentials
to CarrierConnection.config.default_billing_number for all dhl_parcel_de connections.
"""

from django.db import migrations


def migrate_billing_number_to_config(apps, schema_editor):
    """Migrate billing_number from credentials to config.default_billing_number."""
    CarrierConnection = apps.get_model("providers", "CarrierConnection")

    carriers = CarrierConnection.objects.filter(carrier_code="dhl_parcel_de")

    for carrier in carriers:
        credentials = carrier.credentials or {}
        billing_number = credentials.pop("billing_number", None)

        if billing_number:
            config = carrier.config or {}
            config["default_billing_number"] = billing_number
            carrier.config = config
            carrier.credentials = credentials
            carrier.save(update_fields=["config", "credentials"])


def reverse_migration(apps, schema_editor):
    """Reverse: move default_billing_number back to credentials."""
    CarrierConnection = apps.get_model("providers", "CarrierConnection")

    carriers = CarrierConnection.objects.filter(carrier_code="dhl_parcel_de")

    for carrier in carriers:
        config = carrier.config or {}
        billing_number = config.pop("default_billing_number", None)

        if billing_number:
            credentials = carrier.credentials or {}
            credentials["billing_number"] = billing_number
            carrier.credentials = credentials
            carrier.config = config
            carrier.save(update_fields=["config", "credentials"])


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0099_cleanup"),
    ]

    operations = [
        migrations.RunPython(
            migrate_billing_number_to_config,
            reverse_migration,
        ),
    ]
