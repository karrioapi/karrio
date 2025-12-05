# Generated migration to fix ManyToMany junction table names
# The RenameField in migration 0010 didn't properly rename the ManyToMany junction tables
# This is a long-standing bug that's now being fixed

from django.db import migrations


# Mapping of old table names to new table names
TABLE_RENAMES = [
    ('customs_shipment_commodities', 'customs_commodities'),
    ('shipment_shipment_parcels', 'shipment_parcels'),
]


def rename_junction_tables(_apps, schema_editor):
    """
    Rename ManyToMany junction tables from old names to new names.
    Uses Django's introspection API for database-agnostic table detection.
    """
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()

    for old_table, new_table in TABLE_RENAMES:
        if old_table in existing_tables and new_table not in existing_tables:
            schema_editor.execute(
                schema_editor.sql_rename_table % {
                    "old_table": schema_editor.quote_name(old_table),
                    "new_table": schema_editor.quote_name(new_table),
                }
            )


def reverse_rename(_apps, schema_editor):
    """Reverse the table renames."""
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()

    for old_table, new_table in TABLE_RENAMES:
        if new_table in existing_tables and old_table not in existing_tables:
            schema_editor.execute(
                schema_editor.sql_rename_table % {
                    "old_table": schema_editor.quote_name(new_table),
                    "new_table": schema_editor.quote_name(old_table),
                }
            )


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0066_commodity_image_url_commodity_product_id_and_more'),
    ]

    operations = [
        migrations.RunPython(rename_junction_tables, reverse_rename),
    ]
