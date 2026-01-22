# Rename Carrier model to CarrierConnection, update table names, and cleanup legacy models

from django.conf import settings
from django.db import migrations


def get_dependencies():
    """Build dependencies list, conditionally including orgs migration."""
    deps = [
        ("providers", "0094_remove_carrier_legacy_fields"),
    ]
    # Only add orgs dependency in multi-org mode (insiders)
    # In OSS mode, orgs module doesn't have this migration
    if getattr(settings, "MULTI_ORGANIZATIONS", False):
        deps.append(("orgs", "0026_remove_organization_system_carriers"))
    return deps


def cleanup_orgs_carrier_config_links(apps, schema_editor):
    """
    Clean up orgs link tables that reference CarrierConfig before deleting the model.
    This handles the case where the database was created in insiders mode but migrations
    are running in OSS mode.

    In insiders mode, orgs.0026_remove_organization_system_carriers runs first (via dependency)
    and handles this cleanup properly. This is a fallback for OSS mode with insiders DB.
    """
    connection = schema_editor.connection
    table_names = connection.introspection.table_names()

    # Try to get orgs link models and clean them up using Django ORM
    try:
        CarrierConfigLink = apps.get_model("orgs", "CarrierConfigLink")
        CarrierConfigLink.objects.all().delete()
    except LookupError:
        # Model not registered - check if table exists
        if "orgs_carrierconfiglink" in table_names:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orgs_carrierconfiglink")

    # Also try to clear any M2M relationships
    try:
        Organization = apps.get_model("orgs", "Organization")
        for org in Organization.objects.all():
            if hasattr(org, "carrier_configs"):
                org.carrier_configs.clear()
            if hasattr(org, "system_carriers"):
                org.system_carriers.clear()
    except LookupError:
        # Models not registered - clean up tables directly if they exist
        tables_to_clean = [
            "orgs_organization_carrier_configs",
            "orgs_organization_system_carriers",
        ]
        for table in tables_to_clean:
            if table in table_names:
                with connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {table}")


def noop(apps, schema_editor):
    """Reverse migration is a no-op since we can't restore deleted links."""
    pass


class Migration(migrations.Migration):
    """
    Rename Carrier model to CarrierConnection, update table names, and delete legacy models.

    Changes:
    - Rename Carrier model to CarrierConnection
    - Rename 'carrier' table to 'CarrierConnection'
    - Rename 'system_connection' table to 'SystemConnection'
    - Rename 'brokered_connection' table to 'BrokeredConnection'
    - Delete CarrierConfig model (replaced by SystemConnection.config and BrokeredConnection.config_overrides)
    """

    dependencies = get_dependencies()

    operations = [
        # Clean up orgs link tables first (handles insiders DB in OSS mode)
        migrations.RunPython(cleanup_orgs_carrier_config_links, noop),
        # Rename the model
        migrations.RenameModel(
            old_name="Carrier",
            new_name="CarrierConnection",
        ),
        # Rename tables to CamelCase
        migrations.AlterModelTable(
            name="carrierconnection",
            table="CarrierConnection",
        ),
        migrations.AlterModelTable(
            name="systemconnection",
            table="SystemConnection",
        ),
        migrations.AlterModelTable(
            name="brokeredconnection",
            table="BrokeredConnection",
        ),
        # Delete legacy CarrierConfig model (data was migrated in 0093)
        migrations.DeleteModel(
            name="CarrierConfig",
        ),
    ]
