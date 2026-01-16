# Clean model refactoring migration
# This migration completes the JSON field migration by:
# 1. Adding JSON address field to Pickup and Manifest
# 2. Populating Pickup and Manifest address data from FK
# 3. Dropping legacy FK/M2M fields from Shipment
# 4. Renaming *_data fields to direct names (removing suffix)
# 5. Renaming tables to plural form

import functools
from django.db import migrations, models
import karrio.server.core.utils


def address_to_dict(address):
    """Convert Address model instance to JSON dict."""
    if address is None:
        return None

    return {
        "id": address.id,
        "object_type": "address",
        "postal_code": address.postal_code,
        "city": address.city,
        "country_code": address.country_code,
        "federal_tax_id": address.federal_tax_id,
        "state_tax_id": address.state_tax_id,
        "person_name": address.person_name,
        "company_name": address.company_name,
        "email": address.email,
        "phone_number": address.phone_number,
        "state_code": address.state_code,
        "suburb": address.suburb,
        "residential": address.residential,
        "street_number": address.street_number,
        "address_line1": address.address_line1,
        "address_line2": address.address_line2,
        "validate_location": address.validate_location,
        "validation": address.validation,
    }


def populate_pickup_manifest_json(apps, schema_editor):
    """Populate JSON address fields for Pickup and Manifest from FK."""
    Pickup = apps.get_model("manager", "Pickup")
    Manifest = apps.get_model("manager", "Manifest")

    # Populate Pickup address_data
    for pickup in Pickup.objects.select_related("address").all():
        if pickup.address and not pickup.address_data:
            pickup.address_data = address_to_dict(pickup.address)
            pickup.save(update_fields=["address_data"])

    # Populate Manifest address_data
    for manifest in Manifest.objects.select_related("address").all():
        if manifest.address and not manifest.address_data:
            manifest.address_data = address_to_dict(manifest.address)
            manifest.save(update_fields=["address_data"])


def reverse_noop(apps, schema_editor):
    """Reverse migration is a no-op."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0073_make_shipment_fk_nullable"),
    ]

    operations = [
        # =========================================================
        # STEP 1: Add JSON fields to Pickup and Manifest
        # =========================================================
        migrations.AddField(
            model_name="pickup",
            name="address_data",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Pickup address (embedded JSON)",
            ),
        ),
        migrations.AddField(
            model_name="manifest",
            name="address_data",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text="Manifest address (embedded JSON)",
            ),
        ),

        # =========================================================
        # STEP 2: Populate JSON fields from FK
        # =========================================================
        migrations.RunPython(
            populate_pickup_manifest_json,
            reverse_noop,
        ),

        # =========================================================
        # STEP 3: Drop Shipment legacy FK/M2M fields
        # =========================================================
        # Drop FK fields (addresses)
        migrations.RemoveField(
            model_name="shipment",
            name="shipper",
        ),
        migrations.RemoveField(
            model_name="shipment",
            name="recipient",
        ),
        migrations.RemoveField(
            model_name="shipment",
            name="return_address",
        ),
        migrations.RemoveField(
            model_name="shipment",
            name="billing_address",
        ),
        migrations.RemoveField(
            model_name="shipment",
            name="customs",
        ),
        # Drop M2M field (parcels)
        migrations.RemoveField(
            model_name="shipment",
            name="parcels",
        ),

        # =========================================================
        # STEP 4: Drop Pickup and Manifest legacy FK fields
        # =========================================================
        migrations.RemoveField(
            model_name="pickup",
            name="address",
        ),
        migrations.RemoveField(
            model_name="manifest",
            name="address",
        ),

        # =========================================================
        # STEP 5: Rename Shipment *_data fields to direct names
        # =========================================================
        migrations.RenameField(
            model_name="shipment",
            old_name="shipper_data",
            new_name="shipper",
        ),
        migrations.RenameField(
            model_name="shipment",
            old_name="recipient_data",
            new_name="recipient",
        ),
        migrations.RenameField(
            model_name="shipment",
            old_name="return_address_data",
            new_name="return_address",
        ),
        migrations.RenameField(
            model_name="shipment",
            old_name="billing_address_data",
            new_name="billing_address",
        ),
        migrations.RenameField(
            model_name="shipment",
            old_name="parcels_data",
            new_name="parcels",
        ),
        migrations.RenameField(
            model_name="shipment",
            old_name="customs_data",
            new_name="customs",
        ),

        # =========================================================
        # STEP 6: Rename Pickup and Manifest address_data fields
        # =========================================================
        migrations.RenameField(
            model_name="pickup",
            old_name="address_data",
            new_name="address",
        ),
        migrations.RenameField(
            model_name="manifest",
            old_name="address_data",
            new_name="address",
        ),

        # =========================================================
        # STEP 7: Rename tables to plural form
        # =========================================================
        migrations.AlterModelTable(
            name="shipment",
            table="shipments",
        ),
        migrations.AlterModelTable(
            name="pickup",
            table="pickups",
        ),
        migrations.AlterModelTable(
            name="manifest",
            table="manifests",
        ),
    ]
