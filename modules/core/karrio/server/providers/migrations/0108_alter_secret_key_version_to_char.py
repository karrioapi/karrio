from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("providers", "0107_update_system_connection_fk")]

    operations = [
        migrations.AlterField(
            model_name="secret",
            name="key_version",
            field=models.CharField(
                max_length=64,
                db_index=True,
                help_text="KEK version used for encryption",
            ),
        ),
    ]
