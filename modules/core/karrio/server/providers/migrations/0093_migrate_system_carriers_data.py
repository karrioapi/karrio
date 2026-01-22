# Data migration: Move system carriers to SystemConnection and create BrokeredConnections
# This migration uses the old is_system and active_users fields before they are removed

from django.db import migrations
from django.conf import settings


def cleanup_orgs_carrier_references(apps, schema_editor, carrier):
    """
    Clean up orgs link tables that reference a carrier before deleting it.
    This handles the case where the database was created in insiders mode but migrations
    are running in OSS mode.

    In insiders mode, the orgs migrations handle this cleanup properly.
    This is a fallback for OSS mode with insiders DB.
    """
    # Try to get orgs link models and clean them up using Django ORM
    try:
        CarrierLink = apps.get_model("orgs", "CarrierLink")
        CarrierLink.objects.filter(item_id=carrier.id).delete()
    except LookupError:
        # Model not registered - check if table exists using Django introspection
        connection = schema_editor.connection
        table_names = connection.introspection.table_names()
        if "orgs_carrierlink" in table_names:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orgs_carrierlink WHERE item_id = %s", [carrier.id])

    # Clear the M2M relationship if it exists
    try:
        if hasattr(carrier, "active_orgs"):
            carrier.active_orgs.clear()
    except Exception:
        # M2M table might exist without the model - clean up directly
        connection = schema_editor.connection
        table_names = connection.introspection.table_names()
        if "orgs_organization_system_carriers" in table_names:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orgs_organization_system_carriers WHERE carrier_id = %s", [carrier.id])


def cleanup_all_orgs_carrier_references(schema_editor):
    """
    Clean up ALL orgs carrier references before migration starts.
    This handles the case where the database was created in insiders mode but migrations
    are running in OSS mode.
    """
    connection = schema_editor.connection
    table_names = connection.introspection.table_names()

    # Clean up all orgs tables that might reference carriers or carrier configs
    tables_to_clean = [
        "orgs_carrierlink",
        "orgs_carrierconfiglink",
        "orgs_organization_system_carriers",
        "orgs_organization_carrier_configs",
    ]

    for table in tables_to_clean:
        if table in table_names:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table}")


def migrate_system_carriers(apps, schema_editor):
    """
    Migrate carriers with is_system=True to SystemConnection.
    Create BrokeredConnections for users/orgs that had access.

    Steps:
    0. Clean up orgs references first (handles insiders DB in OSS mode)
    1. Find all carriers where is_system=True
    2. Create SystemConnection for each
    3. Get CarrierConfig for system config (if any)
    4. Create BrokeredConnection for each user in active_users (OSS)
       or each org in active_orgs (Insiders mode)
    5. Copy user/org-specific CarrierConfig to BrokeredConnection.config_overrides
    6. Delete the original Carrier record
    """
    # Step 0: Clean up orgs references first
    cleanup_all_orgs_carrier_references(schema_editor)

    Carrier = apps.get_model("providers", "Carrier")
    SystemConnection = apps.get_model("providers", "SystemConnection")
    BrokeredConnection = apps.get_model("providers", "BrokeredConnection")
    CarrierConfig = apps.get_model("providers", "CarrierConfig")

    # Check if orgs module is installed
    try:
        Organization = apps.get_model("orgs", "Organization")
        BrokeredConnectionLink = apps.get_model("orgs", "BrokeredConnectionLink")
        has_orgs = True
    except LookupError:
        has_orgs = False

    # Find all system carriers
    system_carriers = Carrier.objects.filter(is_system=True)

    for carrier in system_carriers:
        # 1. Create SystemConnection
        system_conn = SystemConnection.objects.create(
            carrier_code=carrier.carrier_code,
            carrier_id=carrier.carrier_id,
            credentials=carrier.credentials or {},
            config={},  # Will be populated from CarrierConfig below
            capabilities=carrier.capabilities or [],
            active=carrier.active,
            test_mode=carrier.test_mode,
            metadata=carrier.metadata or {},
            created_by=carrier.created_by,
            rate_sheet=carrier.rate_sheet,
        )

        # 2. Get system-level CarrierConfig (created by staff, no org)
        system_config = None
        try:
            system_configs = CarrierConfig.objects.filter(
                carrier=carrier,
                created_by__is_staff=True,
            )
            # In orgs mode, also filter by org=None
            if has_orgs:
                system_configs = system_configs.filter(
                    link__isnull=True
                )
            system_config = system_configs.first()
        except Exception:
            pass

        if system_config:
            system_conn.config = system_config.config or {}
            system_conn.save()

        # 3. Create BrokeredConnections for users/orgs with access
        if has_orgs and settings.MULTI_ORGANIZATIONS:
            # Insiders mode: Create for each org that has access
            # active_orgs is a M2M via Organization.system_carriers
            try:
                for org in carrier.active_orgs.all():
                    # Find org-specific config
                    org_config = CarrierConfig.objects.filter(
                        carrier=carrier,
                        link__org=org,
                    ).first()

                    brokered = BrokeredConnection.objects.create(
                        system_connection=system_conn,
                        carrier_id=system_conn.carrier_id,  # Copy from system connection
                        config_overrides=org_config.config if org_config else {},
                        capabilities_overrides=[],
                        is_enabled=True,
                        metadata={},
                        created_by=None,  # Org-scoped, no specific user
                    )

                    # Create org link
                    BrokeredConnectionLink.objects.create(
                        org=org,
                        item=brokered,
                    )
            except Exception:
                pass  # active_orgs may not exist in schema yet
        else:
            # OSS mode: Create for each user in active_users
            try:
                for user in carrier.active_users.all():
                    # Find user-specific config
                    user_config = CarrierConfig.objects.filter(
                        carrier=carrier,
                        created_by=user,
                    ).first()

                    BrokeredConnection.objects.create(
                        system_connection=system_conn,
                        carrier_id=system_conn.carrier_id,  # Copy from system connection
                        config_overrides=user_config.config if user_config else {},
                        capabilities_overrides=[],
                        is_enabled=True,
                        metadata={},
                        created_by=user,
                    )
            except Exception:
                pass  # active_users may not exist in schema yet

        # 4. Delete the original Carrier record (orgs refs already cleaned up at start)
        carrier.delete()


def reverse_migration(apps, schema_editor):
    """
    Reverse migration: Move SystemConnections back to Carrier with is_system=True.

    Note: This is a best-effort reverse. Some data may be lost (e.g., brokered config overrides
    that can't be cleanly mapped back to CarrierConfig).
    """
    Carrier = apps.get_model("providers", "Carrier")
    SystemConnection = apps.get_model("providers", "SystemConnection")
    BrokeredConnection = apps.get_model("providers", "BrokeredConnection")

    for system_conn in SystemConnection.objects.all():
        # Recreate Carrier
        carrier = Carrier.objects.create(
            carrier_code=system_conn.carrier_code,
            carrier_id=system_conn.carrier_id,
            credentials=system_conn.credentials or {},
            config={},
            capabilities=system_conn.capabilities or [],
            active=system_conn.active,
            is_system=True,
            test_mode=system_conn.test_mode,
            metadata=system_conn.metadata or {},
            created_by=system_conn.created_by,
            rate_sheet=system_conn.rate_sheet,
        )

        # Re-add users to active_users from BrokeredConnections
        for brokered in BrokeredConnection.objects.filter(system_connection=system_conn):
            if brokered.created_by:
                try:
                    carrier.active_users.add(brokered.created_by)
                except Exception:
                    pass

        # Delete SystemConnection and BrokeredConnections
        BrokeredConnection.objects.filter(system_connection=system_conn).delete()
        system_conn.delete()


class Migration(migrations.Migration):
    """
    Step 2: Data migration - Move system carriers to SystemConnection.

    This migration:
    - Moves Carriers with is_system=True to SystemConnection
    - Creates BrokeredConnections for users/orgs with access
    - Copies CarrierConfig to appropriate places
    - Deletes original Carrier records
    """

    dependencies = [
        ("providers", "0092_add_system_brokered_connection_models_update_carrier"),
        # Depend on orgs migration if orgs module is installed
        # This ensures BrokeredConnectionLink exists for org-scoped migrations
    ]

    # Note: orgs.0025 dependency is optional (only needed for Insiders)
    # The migration handles both OSS and Insiders mode gracefully

    operations = [
        migrations.RunPython(migrate_system_carriers, reverse_migration),
    ]
