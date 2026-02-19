from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_add_generic_fk_to_metafield"),
    ]

    operations = [
        migrations.AddField(
            model_name="apilogindex",
            name="request_id",
            field=models.CharField(max_length=200, null=True, db_index=True),
        ),
    ]
