# Data migration: Surcharge -> Markup

from django.db import migrations


def migrate_surcharges_to_markups(apps, schema_editor):
    """
    Migrate existing Surcharge records to new Markup model.

    Mappings:
    - id: chrg_xxx -> mkp_xxx (preserve original ID for fee tracking)
    - surcharge_type -> markup_type
    - carriers -> carrier_codes
    - services -> service_codes
    - carrier_accounts (M2M) -> connection_ids (JSONField)
    """
    Surcharge = apps.get_model("pricing", "Surcharge")
    Markup = apps.get_model("pricing", "Markup")

    for surcharge in Surcharge.objects.all():
        # Get carrier account IDs from M2M relation
        connection_ids = list(
            surcharge.carrier_accounts.values_list("id", flat=True)
        )

        # Create Markup record with mapped data
        # Preserve original ID to maintain fee tracking
        Markup.objects.create(
            id=surcharge.id,  # Keep original ID (chrg_xxx)
            name=surcharge.name,
            active=surcharge.active,
            amount=surcharge.amount,
            markup_type=surcharge.surcharge_type,  # Same values (AMOUNT/PERCENTAGE)
            is_visible=True,  # New field, default visible
            carrier_codes=surcharge.carriers or [],
            service_codes=surcharge.services or [],
            connection_ids=connection_ids,
            metadata={},
            created_at=surcharge.created_at,
            updated_at=surcharge.updated_at,
        )

        print(f"Migrated surcharge {surcharge.id} -> markup")


def reverse_migration(apps, schema_editor):
    """
    Reverse the migration by clearing Markup table.
    Note: This doesn't restore Surcharge data - use with caution.
    """
    Markup = apps.get_model("pricing", "Markup")
    Markup.objects.all().delete()
    print("Cleared Markup table")


class Migration(migrations.Migration):
    """
    Data migration to convert Surcharge records to Markup records.
    """

    dependencies = [
        ("pricing", "0076_create_markup_and_fee_models"),
    ]

    operations = [
        migrations.RunPython(
            migrate_surcharges_to_markups,
            reverse_migration,
        ),
    ]
