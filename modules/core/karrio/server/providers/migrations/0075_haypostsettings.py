# Generated by Django 4.2.14 on 2024-07-27 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0074_eshippersettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="HayPostSettings",
            fields=[
                (
                    "carrier_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="providers.carrier",
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("customer_id", models.CharField(max_length=100)),
                ("customer_type", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Hay Post Settings",
                "verbose_name_plural": "Hay Post Settings",
                "db_table": "hay-post-settings",
            },
            bases=("providers.carrier",),
        ),
    ]
