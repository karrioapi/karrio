# Generated migration to add index to APIRequestLog table for archiving performance

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_metafield_type_alter_metafield_value'),
    ]

    operations = [
        migrations.RunSQL(
            # Create index on requested_at for archiving queries
            sql=[
                "CREATE INDEX IF NOT EXISTS api_log_requested_at_idx ON rest_framework_tracking_apirequestlog (requested_at);",
            ],
            reverse_sql=[
                "DROP INDEX IF EXISTS api_log_requested_at_idx;",
            ],
        ),
    ]