# Add indexes on JSONFields for query optimization

from django.db import migrations, connection


def create_gin_indexes(apps, schema_editor):
    """Create GIN indexes for PostgreSQL only."""
    if "postgresql" not in connection.vendor:
        return  # Skip for non-PostgreSQL databases

    with connection.cursor() as cursor:
        # Order GIN indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "order_shipping_to_gin_idx"
            ON "orders" USING gin ("shipping_to" jsonb_path_ops)
            WHERE "shipping_to" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "order_options_gin_idx"
            ON "orders" USING gin ("options" jsonb_path_ops)
            WHERE "options" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "order_metadata_gin_idx"
            ON "orders" USING gin ("metadata" jsonb_path_ops)
            WHERE "metadata" IS NOT NULL;
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS "order_line_items_gin_idx"
            ON "orders" USING gin ("line_items" jsonb_path_ops)
            WHERE "line_items" IS NOT NULL;
        """)


def drop_gin_indexes(apps, schema_editor):
    """Drop GIN indexes (reverse migration)."""
    if "postgresql" not in connection.vendor:
        return

    with connection.cursor() as cursor:
        cursor.execute('DROP INDEX IF EXISTS "order_shipping_to_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "order_options_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "order_metadata_gin_idx";')
        cursor.execute('DROP INDEX IF EXISTS "order_line_items_gin_idx";')


class Migration(migrations.Migration):
    """
    Add GIN indexes on Order JSONFields for performance optimization.

    These indexes improve query performance for:
    - Address search (shipping_to fields)
    - Options/metadata has_key lookups
    - Line items queries

    Notes:
    - PostgreSQL: Full GIN index support for JSON containment queries
    - SQLite/MySQL: Indexes skipped via connection.vendor check
    """

    dependencies = [
        ("orders", "0023_clean_model_refactoring"),
    ]

    operations = [
        migrations.RunPython(create_gin_indexes, drop_gin_indexes),
    ]
