# Add indexes on JSONFields for query optimization

import django.db.models as models
import django.db.models.fields.json as json_fields
from django.db import migrations, connection


def create_gin_indexes(apps, schema_editor):
    """Create GIN indexes for PostgreSQL only."""
    if "postgresql" not in connection.vendor:
        return  # Skip for non-PostgreSQL databases

    with connection.cursor() as cursor:
        # Shipment GIN indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "shipment_meta_gin_idx"
            ON "shipments" USING gin ("meta" jsonb_path_ops)
            WHERE "meta" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "shipment_options_gin_idx"
            ON "shipments" USING gin ("options" jsonb_path_ops)
            WHERE "options" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "shipment_metadata_gin_idx"
            ON "shipments" USING gin ("metadata" jsonb_path_ops)
            WHERE "metadata" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "shipment_recipient_gin_idx"
            ON "shipments" USING gin ("recipient" jsonb_path_ops)
            WHERE "recipient" IS NOT NULL;
        """)

        # Tracking GIN indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "tracking_meta_gin_idx"
            ON "tracking-status" USING gin ("meta" jsonb_path_ops)
            WHERE "meta" IS NOT NULL;
        """)

        # Pickup GIN index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "pickup_address_gin_idx"
            ON "pickups" USING gin ("address" jsonb_path_ops)
            WHERE "address" IS NOT NULL;
        """)


def drop_gin_indexes(apps, schema_editor):
    """Drop GIN indexes (reverse migration)."""
    if "postgresql" not in connection.vendor:
        return

    with connection.cursor() as cursor:
        cursor.execute('DROP INDEX IF EXISTS "shipment_meta_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "shipment_options_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "shipment_metadata_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "shipment_recipient_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "tracking_meta_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "pickup_address_gin_idx";')


class Migration(migrations.Migration):
    """
    Step 4: Add indexes on JSONFields for performance optimization.

    Index Types:
    1. KeyTextTransform indexes - For exact match queries on specific JSON keys
       - carrier.carrier_code, carrier.connection_id
    2. GIN indexes (PostgreSQL only) - For has_key, contains, and varied lookups
       - meta, options, metadata, recipient fields

    Notes:
    - PostgreSQL: Full support for both index types
    - SQLite: KeyTextTransform indexes created but not used; GIN indexes skipped
    - Conditional indexes avoid indexing NULL values to save space
    """

    dependencies = [
        ("manager", "0079_remove_carrier_fk_fields"),
    ]

    operations = [
        # ─────────────────────────────────────────────────────────────────
        # CARRIER SNAPSHOT INDEXES (KeyTextTransform - exact match queries)
        # ─────────────────────────────────────────────────────────────────

        # Shipment.carrier.carrier_code index
        # Used by: ShipmentFilters.carrier_filter, ManifestSerializer shipment filter
        migrations.AddIndex(
            model_name="shipment",
            index=models.Index(
                json_fields.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="shipment_carrier_code_idx",
            ),
        ),
        # Tracking.carrier.carrier_code index
        # Used by: TrackerFilters.carrier_filter, tracker views
        migrations.AddIndex(
            model_name="tracking",
            index=models.Index(
                json_fields.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="tracking_carrier_code_idx",
            ),
        ),
        # Tracking.carrier.connection_id index
        # Used by: CarrierConnection serializer to find related trackers
        migrations.AddIndex(
            model_name="tracking",
            index=models.Index(
                json_fields.KeyTextTransform("connection_id", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="tracking_connection_id_idx",
            ),
        ),
        # Manifest.carrier.carrier_code index
        # Used by: ManifestFilters.carrier_filter
        migrations.AddIndex(
            model_name="manifest",
            index=models.Index(
                json_fields.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="manifest_carrier_code_idx",
            ),
        ),

        # ─────────────────────────────────────────────────────────────────
        # GIN INDEXES (PostgreSQL only - for has_key, contains, text search)
        # ─────────────────────────────────────────────────────────────────
        # These indexes support: __has_key, __contains, __icontains on JSON keys
        # RunPython is used to conditionally create indexes based on DB vendor
        migrations.RunPython(create_gin_indexes, drop_gin_indexes),
    ]
