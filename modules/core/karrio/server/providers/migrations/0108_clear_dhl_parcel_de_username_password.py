"""Clear username and password from dhl_parcel_de connections.

These credentials are now provided by system configuration and should not
be stored per-connection. This migration removes existing values from both
CarrierConnection and SystemConnection.
"""

from django.db import migrations


def clear_username_password(apps, schema_editor):
    """Remove username and password from dhl_parcel_de connections."""
    CarrierConnection = apps.get_model("providers", "CarrierConnection")
    SystemConnection = apps.get_model("providers", "SystemConnection")

    for Model in [CarrierConnection, SystemConnection]:
        carriers = Model.objects.filter(carrier_code="dhl_parcel_de")

        for carrier in carriers:
            credentials = carrier.credentials or {}
            changed = False

            if "username" in credentials:
                credentials.pop("username")
                changed = True
            if "password" in credentials:
                credentials.pop("password")
                changed = True

            if changed:
                carrier.credentials = credentials
                carrier.save(update_fields=["credentials"])


def reverse_migration(apps, schema_editor):
    """No-op reverse: cannot restore cleared credentials."""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0107_update_system_connection_fk"),
    ]

    operations = [
        migrations.RunPython(
            clear_username_password,
            reverse_migration,
        ),
    ]
