from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0108_alter_secret_key_version_to_char"),
        ("providers", "0109_cleanup_legacy_system_rate_sheets"),
    ]

    operations = []
