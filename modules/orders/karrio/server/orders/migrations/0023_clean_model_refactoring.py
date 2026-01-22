# Clean model refactoring migration for Orders
# This migration completes the JSON field migration by:
# 1. Dropping legacy FK/M2M fields from Order
# 2. Deleting the OrderLineItemLink through table
# 3. Renaming *_data fields to direct names (removing suffix)
# 4. Renaming table to plural form

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0022_make_order_fk_nullable"),
        ("manager", "0074_clean_model_refactoring"),  # Ensure manager migration runs first
    ]

    operations = [
        # =========================================================
        # STEP 1: Drop Order legacy FK/M2M fields
        # =========================================================
        # Drop FK fields (addresses)
        migrations.RemoveField(
            model_name="order",
            name="shipping_to",
        ),
        migrations.RemoveField(
            model_name="order",
            name="shipping_from",
        ),
        migrations.RemoveField(
            model_name="order",
            name="billing_address",
        ),
        # Drop M2M field (line_items) - this also removes the through table reference
        migrations.RemoveField(
            model_name="order",
            name="line_items",
        ),

        # =========================================================
        # STEP 2: Delete OrderLineItemLink through model
        # =========================================================
        migrations.DeleteModel(
            name="OrderLineItemLink",
        ),

        # =========================================================
        # STEP 3: Rename *_data fields to direct names
        # =========================================================
        migrations.RenameField(
            model_name="order",
            old_name="shipping_to_data",
            new_name="shipping_to",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="shipping_from_data",
            new_name="shipping_from",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="billing_address_data",
            new_name="billing_address",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="line_items_data",
            new_name="line_items",
        ),

        # =========================================================
        # STEP 4: Rename table to plural form
        # =========================================================
        migrations.AlterModelTable(
            name="order",
            table="orders",
        ),
    ]
