"""Add 'pickup' to capabilities for existing dhl_parcel_de connections."""

from django.db import migrations


def add_pickup_capability(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for model_name in ("CarrierConnection", "SystemConnection"):
        Model = apps.get_model("providers", model_name)
        for conn in (
            Model.objects.using(db_alias)
            .filter(carrier_code="dhl_parcel_de")
            .iterator()
        ):
            capabilities = conn.capabilities or []
            if "pickup" not in capabilities:
                conn.capabilities = [*capabilities, "pickup"]
                conn.save(update_fields=["capabilities"])


def remove_pickup_capability(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for model_name in ("CarrierConnection", "SystemConnection"):
        Model = apps.get_model("providers", model_name)
        for conn in (
            Model.objects.using(db_alias)
            .filter(carrier_code="dhl_parcel_de")
            .iterator()
        ):
            capabilities = conn.capabilities or []
            if "pickup" in capabilities:
                conn.capabilities = [c for c in capabilities if c != "pickup"]
                conn.save(update_fields=["capabilities"])


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0100_migrate_dhl_parcel_de_billing_number"),
    ]

    operations = [
        migrations.RunPython(add_pickup_capability, remove_pickup_capability),
    ]
