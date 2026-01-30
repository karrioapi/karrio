"""
Migration: Convert Fee model from FK-based to denormalized snapshot model.

Changes:
- Replace FK shipment → CharField shipment_id (snapshot)
- Replace FK markup → CharField markup_id (snapshot)
- Add account_id CharField (org context snapshot)
- Add test_mode BooleanField
- Rename markup_type → fee_type
- Rename markup_percentage → percentage
- Add composite indexes for time-series queries
- Data migration: populate account_id and test_mode from shipment data

Strategy for FK → CharField conversion:
1. Add temporary CharField fields (_shipment_id, _markup_id)
2. Data migration: copy FK values to temp fields
3. Remove FK fields (drops constraints automatically)
4. Rename temp fields to final names
This is fully portable across SQLite, PostgreSQL, and MySQL.
"""

from django.db import migrations, models


def copy_fk_values_to_temp_fields(apps, schema_editor):
    """Copy FK IDs to temporary CharField fields before dropping FKs."""
    Fee = apps.get_model("pricing", "Fee")
    batch_size = 500
    update_batch = []

    for fee in Fee.objects.all().iterator(chunk_size=batch_size):
        fee._shipment_id = fee.shipment_id or ""
        fee._markup_id = fee.markup_id
        update_batch.append(fee)

        if len(update_batch) >= batch_size:
            Fee.objects.bulk_update(
                update_batch, ["_shipment_id", "_markup_id"], batch_size=batch_size
            )
            update_batch = []

    if update_batch:
        Fee.objects.bulk_update(
            update_batch, ["_shipment_id", "_markup_id"], batch_size=batch_size
        )


def populate_snapshot_fields(apps, schema_editor):
    """Populate account_id and test_mode from existing shipment data."""
    Fee = apps.get_model("pricing", "Fee")
    batch_size = 500

    # Populate test_mode from shipment
    try:
        Shipment = apps.get_model("manager", "Shipment")
        shipment_ids = list(
            Fee.objects.values_list("shipment_id", flat=True).distinct()[:10000]
        )
        test_mode_map = dict(
            Shipment.objects.filter(id__in=shipment_ids)
            .values_list("id", "test_mode")
        )

        update_batch = []
        for fee in Fee.objects.all().iterator(chunk_size=batch_size):
            test_mode = test_mode_map.get(fee.shipment_id, False)
            if test_mode:
                fee.test_mode = test_mode
                update_batch.append(fee)
            if len(update_batch) >= batch_size:
                Fee.objects.bulk_update(update_batch, ["test_mode"], batch_size=batch_size)
                update_batch = []
        if update_batch:
            Fee.objects.bulk_update(update_batch, ["test_mode"], batch_size=batch_size)
    except LookupError:
        pass

    # Populate account_id from shipment org links
    try:
        ShipmentLink = apps.get_model("orgs", "ShipmentLink")
        shipment_ids = list(
            Fee.objects.filter(account_id__isnull=True)
            .values_list("shipment_id", flat=True)
            .distinct()[:10000]
        )
        link_map = dict(
            ShipmentLink.objects.filter(item_id__in=shipment_ids)
            .values_list("item_id", "org_id")
        )

        update_batch = []
        for fee in Fee.objects.filter(account_id__isnull=True).iterator(chunk_size=batch_size):
            org_id = link_map.get(fee.shipment_id)
            if org_id:
                fee.account_id = org_id
                update_batch.append(fee)
            if len(update_batch) >= batch_size:
                Fee.objects.bulk_update(update_batch, ["account_id"], batch_size=batch_size)
                update_batch = []
        if update_batch:
            Fee.objects.bulk_update(update_batch, ["account_id"], batch_size=batch_size)
    except LookupError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("pricing", "0078_cleanup"),
    ]

    operations = [
        # ─── Step 1: Remove old indexes ──────────────────────────────────
        migrations.RemoveIndex(
            model_name="fee",
            name="fee_shipmen_cf6644_idx",
        ),
        migrations.RemoveIndex(
            model_name="fee",
            name="fee_markup__6438ea_idx",
        ),
        migrations.RemoveIndex(
            model_name="fee",
            name="fee_carrier_86bb46_idx",
        ),
        migrations.RemoveIndex(
            model_name="fee",
            name="fee_created_050ccc_idx",
        ),

        # ─── Step 2: Add temporary CharField fields to hold FK values ────
        migrations.AddField(
            model_name="fee",
            name="_shipment_id",
            field=models.CharField(
                max_length=50,
                default="",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fee",
            name="_markup_id",
            field=models.CharField(
                max_length=50,
                null=True,
                blank=True,
            ),
        ),

        # ─── Step 3: Copy FK values to temp fields ──────────────────────
        migrations.RunPython(
            copy_fk_values_to_temp_fields,
            migrations.RunPython.noop,
        ),

        # ─── Step 4: Remove FK fields (drops constraints automatically) ─
        migrations.RemoveField(
            model_name="fee",
            name="shipment",
        ),
        migrations.RemoveField(
            model_name="fee",
            name="markup",
        ),

        # ─── Step 5: Rename temp fields to final names ──────────────────
        migrations.RenameField(
            model_name="fee",
            old_name="_shipment_id",
            new_name="shipment_id",
        ),
        migrations.RenameField(
            model_name="fee",
            old_name="_markup_id",
            new_name="markup_id",
        ),

        # ─── Step 6: Update field attributes (add indexes, help_text) ───
        migrations.AlterField(
            model_name="fee",
            name="shipment_id",
            field=models.CharField(
                max_length=50,
                db_index=True,
                help_text="The shipment this fee was applied to",
            ),
        ),
        migrations.AlterField(
            model_name="fee",
            name="markup_id",
            field=models.CharField(
                max_length=50,
                null=True,
                blank=True,
                db_index=True,
                help_text="The markup ID that generated this fee",
            ),
        ),

        # ─── Step 7: Rename existing fields ─────────────────────────────
        migrations.RenameField(
            model_name="fee",
            old_name="markup_type",
            new_name="fee_type",
        ),
        migrations.RenameField(
            model_name="fee",
            old_name="markup_percentage",
            new_name="percentage",
        ),

        # ─── Step 8: Add new snapshot fields ─────────────────────────────
        migrations.AddField(
            model_name="fee",
            name="account_id",
            field=models.CharField(
                max_length=50,
                null=True,
                blank=True,
                db_index=True,
                help_text="The organization/account this fee belongs to",
            ),
        ),
        migrations.AddField(
            model_name="fee",
            name="test_mode",
            field=models.BooleanField(default=False),
        ),

        # ─── Step 9: Update connection_id to be indexed ─────────────────
        migrations.AlterField(
            model_name="fee",
            name="connection_id",
            field=models.CharField(
                max_length=50,
                db_index=True,
                help_text="Connection ID used for this shipment",
            ),
        ),

        # ─── Step 10: Data migration — populate snapshot fields ─────────
        migrations.RunPython(
            populate_snapshot_fields,
            migrations.RunPython.noop,
        ),

        # ─── Step 11: Add indexes ───────────────────────────────────────
        # Single-field indexes for fields without db_index=True
        # (shipment_id, markup_id, account_id, connection_id already
        #  get indexes via db_index=True on the field definition)
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(
                fields=["carrier_code"], name="fee_carrier_86bb46_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(
                fields=["created_at"], name="fee_created_050ccc_idx"
            ),
        ),
        # Composite indexes for time-series queries
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(
                fields=["account_id", "created_at"], name="fee_account_507a12_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(
                fields=["connection_id", "created_at"], name="fee_connect_3aeeec_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(
                fields=["markup_id", "created_at"], name="fee_markup__130c94_idx"
            ),
        ),
    ]
